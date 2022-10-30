from schedule import Scheduler
import asyncio

def job(id):
    print("im working", id)


scheduler = Scheduler()
scheduler.every(1).second.at("12:50:30").do(target=job, args=(1,))
scheduler.every(2).second.at("12:50:30").do(target=job, args=(2,))
scheduler.every(3).second.at("12:50:30").do(target=job, args=(3,))
scheduler.every(4).second.at("12:50:30").do(target=job, args=(4,))
scheduler.every(5).second.at("12:50:30").do(target=job, args=(5,))
scheduler.every(6).second.at("12:50:30").do(target=job, args=(6,))
scheduler.every(7).second.at("12:50:30").do(target=job, args=(7,))
scheduler.every(8).second.at("12:50:30").do(target=job, args=(8,))
asyncio.run(scheduler.run())
