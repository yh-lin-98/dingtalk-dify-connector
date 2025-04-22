#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from loguru import logger
from agent import AgentLoop

def main():
    logger.info('start dingtalk dify connector ...')
    agent = AgentLoop()
    agent.run_forever()

if __name__ == '__main__':
    main()