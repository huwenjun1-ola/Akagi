import os
import sys

from entry import entry
from loguru import logger as main_logger

if __name__ == '__main__':
    if os.environ.get("LOGURU_WRITEFILE", "1") == "0":
        main_logger.remove()
        # 2. 重新添加：仅绑定标准输出和标准错误
        # 通常建议：INFO 及以下去 stdout，WARNING 及以上去 stderr
        main_logger.add(sys.stdout, level="DEBUG")
        main_logger.add(sys.stderr, level="WARNING")
    entry.main()