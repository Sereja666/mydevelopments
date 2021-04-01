#!venv/bin/python
from aiogram import executor

# Если запускаете код отдельно от этого репозитория, то закомментируйте эти две строки...
from aiogrambot.misc import dp
import aiogrambot.handlers
# ... и раскомментируйте эти
# from misc import dp
# import handlers


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)