# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""WebGraph driver

"""

import logging
import os
import subprocess

from enum import Enum
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

import psutil

from click import ParamType

from swh.graph.backend import find_graph_jar


class CompressionStep(Enum):
    MPH = 1
    BV = 2
    BV_OBL = 3
    BFS = 4
    PERMUTE = 5
    PERMUTE_OBL = 6
    STATS = 7
    TRANSPOSE = 8
    TRANSPOSE_OBL = 9
    MAPS = 10
    CLEAN_TMP = 11

    def __str__(self):
        return self.name


# full compression pipeline
COMP_SEQ = list(CompressionStep)

# Mapping from compression steps to shell commands implementing them. Commands
# will be executed by the shell, so be careful with meta characters. They are
# specified here as lists of tokens that will be joined together only for ease
# of line splitting. In commands, {tokens} will be interpolated with
# configuration values, see :func:`compress`.
STEP_ARGV = {
    CompressionStep.MPH:
    ['zcat', '{in_dir}/{graph_name}.nodes.csv.gz', '|',
     '{java}', 'it.unimi.dsi.sux4j.mph.GOVMinimalPerfectHashFunction',
     '--temp-dir', '{tmp_dir}', '{out_dir}/{graph_name}.mph'],
    CompressionStep.BV:
    ['zcat', '{in_dir}/{graph_name}.edges.csv.gz', '|',
     '{java}', 'it.unimi.dsi.big.webgraph.ScatteredArcsASCIIGraph',
     '--temp-dir', '{tmp_dir}',
     '--function', '{out_dir}/{graph_name}.mph', '{out_dir}/{graph_name}-bv'],
    CompressionStep.BV_OBL:
    ['{java}', 'it.unimi.dsi.big.webgraph.BVGraph',
     '--list', '{out_dir}/{graph_name}-bv'],
    CompressionStep.BFS:
    ['{java}', 'it.unimi.dsi.law.big.graph.BFS',
     '{out_dir}/{graph_name}-bv', '{out_dir}/{graph_name}.order'],
    CompressionStep.PERMUTE:
    ['{java}', 'it.unimi.dsi.big.webgraph.Transform',
     'mapOffline', '{out_dir}/{graph_name}-bv', '{out_dir}/{graph_name}',
     '{out_dir}/{graph_name}.order', '{batch_size}', '{tmp_dir}'],
    CompressionStep.PERMUTE_OBL:
    ['{java}', 'it.unimi.dsi.big.webgraph.BVGraph',
     '--list', '{out_dir}/{graph_name}'],
    CompressionStep.STATS:
    ['{java}', 'it.unimi.dsi.big.webgraph.Stats',
     '{out_dir}/{graph_name}'],
    CompressionStep.TRANSPOSE:
    ['{java}', 'it.unimi.dsi.big.webgraph.Transform',
     'transposeOffline', '{out_dir}/{graph_name}',
     '{out_dir}/{graph_name}-transposed', '{batch_size}', '{tmp_dir}'],
    CompressionStep.TRANSPOSE_OBL:
    ['{java}', 'it.unimi.dsi.big.webgraph.BVGraph',
     '--list', '{out_dir}/{graph_name}-transposed'],
    CompressionStep.MAPS:
    ['{java}', 'org.softwareheritage.graph.backend.Setup',
     '{in_dir}/{graph_name}.nodes.csv.gz', '{out_dir}/{graph_name}'],
    CompressionStep.CLEAN_TMP:
    ['rm', '-rf',
     '{out_dir}/{graph_name}-bv.graph',
     '{out_dir}/{graph_name}-bv.obl',
     '{out_dir}/{graph_name}-bv.offsets',
     '{tmp_dir}'],
}  # type: Dict[CompressionStep, List[str]]


class StepOption(ParamType):
    """click type for specifying a compression step on the CLI

    parse either individual steps, specified as step names or integers, or step
    ranges

    """
    name = "compression step"

    def convert(self, value, param, ctx) -> Set[CompressionStep]:
        steps = set()  # type: Set[CompressionStep]

        specs = value.split(',')
        for spec in specs:
            if '-' in spec:  # step range
                (raw_l, raw_r) = spec.split('-', maxsplit=1)
                if raw_l == '':  # no left endpoint
                    raw_l = COMP_SEQ[0].name
                if raw_r == '':  # no right endpoint
                    raw_r = COMP_SEQ[-1].name
                l_step = self.convert(raw_l, param, ctx)
                r_step = self.convert(raw_r, param, ctx)
                if len(l_step) != 1 or len(r_step) != 1:
                    self.fail('invalid step specification: %s, see --help'
                              % value)
                l_idx = l_step.pop()
                r_idx = r_step.pop()
                steps = steps.union(set(map(CompressionStep,
                                            range(l_idx.value,
                                                  r_idx.value + 1))))
            else:  # singleton step
                try:
                    steps.add(CompressionStep(int(spec)))  # integer step
                except ValueError:
                    try:
                        steps.add(CompressionStep[spec.upper()])  # step name
                    except KeyError:
                        self.fail('invalid step specification: %s, see --help'
                                  % value)

        return steps


def do_step(step, conf):
    cmd = ' '.join(STEP_ARGV[step]).format(**conf)

    cmd_env = os.environ.copy()
    cmd_env['JAVA_TOOL_OPTIONS'] = conf['java_tool_options']
    cmd_env['CLASSPATH'] = conf['classpath']

    logging.info('running: %s' % cmd)
    process = subprocess.Popen(cmd, shell=True,
                               env=cmd_env, encoding='utf8',
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    with process.stdout as stdout:
        for line in stdout:
            logging.info(line.rstrip())
    rc = process.wait()
    if rc != 0:
        raise RuntimeError('compression step %s returned non-zero '
                           'exit code %d' % (step, rc))
    else:
        return rc


def check_config(conf, graph_name, in_dir, out_dir):
    """check compression configuration, propagate defaults, and initialize
    execution environment

    """
    conf = conf.copy()
    conf['graph_name'] = graph_name
    conf['in_dir'] = str(in_dir)
    conf['out_dir'] = str(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if 'tmp_dir' not in conf:
        tmp_dir = out_dir / 'tmp'
        conf['tmp_dir'] = str(tmp_dir)
    else:
        tmp_dir = Path(conf['tmp_dir'])
    tmp_dir.mkdir(parents=True, exist_ok=True)
    if 'batch_size' not in conf:
        conf['batch_size'] = '1000000000'  # 1 billion
    if 'logback' not in conf:
        logback_confpath = tmp_dir / 'logback.xml'
        with open(logback_confpath, 'w') as conffile:
            conffile.write("""
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d %r %p [%t] %logger{1} - %m%n</pattern>
        </encoder>
    </appender>
    <root level="INFO">
        <appender-ref ref="STDOUT"/>
    </root>
</configuration>
""")
        conf['logback'] = str(logback_confpath)
    if 'max_ram' not in conf:
        conf['max_ram'] = str(psutil.virtual_memory().total)
    if 'java_tool_options' not in conf:
        assert 'logback' in conf
        conf['java_tool_options'] = ' '.join([
            '-Xmx{max_ram}', '-XX:PretenureSizeThreshold=512M',
            '-XX:MaxNewSize=4G', '-XX:+UseLargePages',
            '-XX:+UseTransparentHugePages', '-XX:+UseNUMA', '-XX:+UseTLAB',
            '-XX:+ResizeTLAB', '-Dlogback.configurationFile={logback}'
        ]).format(max_ram=conf['max_ram'], logback=conf['logback'])
    if 'java' not in conf:
        conf['java'] = 'java'
    if 'classpath' not in conf:
        conf['classpath'] = find_graph_jar()

    return conf


def compress(graph_name: str, in_dir: Path, out_dir: Path,
             steps: Set[CompressionStep] = set(COMP_SEQ),
             conf: Dict[str, str] = {}):
    """graph compression pipeline driver from nodes/edges files to compressed
    on-disk representation

    Args:
        graph_name: graph base name, relative to in_dir
        in_dir: input directory, where the uncompressed graph can be found
        out_dir: output directory, where the compressed graph will be stored
        steps: compression steps to run (default: all steps)
        conf: compression configuration, supporting the following keys (all are
          optional, so an empty configuration is fine and is the default)

          - batch_size: batch size for `WebGraph transformations
            <http://webgraph.di.unimi.it/docs/it/unimi/dsi/webgraph/Transform.html>`_;
            defaults to 1 billion
          - classpath: java classpath, defaults to swh-graph JAR only
          - java: command to run java VM, defaults to "java"
          - java_tool_options: value for JAVA_TOOL_OPTIONS environment
            variable; defaults to various settings for high memory machines
          - logback: path to a logback.xml configuration file; if not provided
            a temporary one will be created and used
          - max_ram: maximum RAM to use for compression; defaults to available
            virtual memory
          - tmp_dir: temporary directory, defaults to the "tmp" subdir of
            out_dir

    """
    if not steps:
        steps = set(COMP_SEQ)

    conf = check_config(conf, graph_name, in_dir, out_dir)

    logging.info('starting compression')
    compression_start_time = datetime.now()
    seq_no = 0
    for step in COMP_SEQ:
        if step not in steps:
            logging.debug('skipping compression step %s' % step)
            continue
        seq_no += 1
        logging.info('starting compression step %s (%d/%d)'
                     % (step, seq_no, len(steps)))
        step_start_time = datetime.now()
        do_step(step, conf)
        step_duration = datetime.now() - step_start_time
        logging.info('completed compression step %s (%d/%d) in %s'
                     % (step, seq_no, len(steps), step_duration))
    compression_duration = datetime.now() - compression_start_time
    logging.info('completed compression in %s' % compression_duration)
