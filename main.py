
import bot
import asyncio
import logging
import sys
import db

if __name__ == "__main__":
    db.createUsers()
    db.createStats()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(bot.main())