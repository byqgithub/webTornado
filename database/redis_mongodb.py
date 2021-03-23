# -*- coding: utf-8 -*-

import asyncio
from aredis import StrictRedis
import motor.motor_tornado
import motor.motor_asyncio

remote_host = "192.168.2.205"
redis_port = '6379'
client = StrictRedis(host=remote_host, port=redis_port)


async def get_string():
    result = await client.get("name")
    print("Redis string key: %s; info: %s" % ("name", str(result)))


async def get_hash():
    result = await client.hgetall("dbs")
    print("Redis hash key: %s; info: %s" % ("dbs", str(result)))
    keys = client.hscan_iter("dbs")
    async for key in keys:
        print("Redis hash iter key: %s" % [key])


async def redis_main():
    task = asyncio.create_task(get_string())
    # done, pending = await asyncio.wait({task})
    # for one in done:
    #     print("Done task info: %s" % one)
    # for two in pending:
    #     print("Pending task info: %s" % two)

    # await example()

    result = await asyncio.gather(get_string(), get_hash())
    print("asyncio.gather result: %s" % result)


async def mongodb_collection_find(current_loop):
    uri = f'mongodb://{"test"}:{"test"}@{remote_host}:{27017}/test?authSource=admin'
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(uri, io_loop=current_loop)
    db = mongo_client["test"]
    collection = db.collection
    async for doc in collection.find({}, {'_id': 0}):
        print("Mongodb test.collection find one result: %s" % doc)


async def mongodb_main():
    loop = asyncio.get_event_loop()
    task = asyncio.create_task(mongodb_collection_find(loop))
    done, pending = await asyncio.wait({task})
    for one in done:
        print("Done task info: %s" % one)


if __name__ == '__main__':
    # asyncio.run(redis_main())

    asyncio.run(mongodb_main())
    # motor 自动启动事件循环，如果使用 asyncio.run 时，需要将当前 loop 赋值给 AsyncIOMotorClient
    # 如果不将 loop 赋值到 AsyncIOMotorClient 中，需要在程序开始前，获取 motor 启动的 loop
    # 注；需要使用 motor.motor_asyncio.AsyncIOMotorClient, motor_tornado 不可以
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(mongodb_main())
