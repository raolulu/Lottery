#!/usr/bin/python
#coding=utf-8
class LotteryInfo:

    def __init__(self, lotteryDrawNum, lotteryDrawResult, lotteryUnsortDrawresult, lotteryDrawTime):
        self.lotteryDrawNum = lotteryDrawNum
        self.lotteryDrawResult = lotteryDrawResult
        self.lotteryUnsortDrawresult = lotteryUnsortDrawresult
        self.lotteryDrawTime = lotteryDrawTime

    def getLotteryDrawNum(self):
        return self.lotteryDrawNum

    def getLotteryDrawResult(self):
        return self.lotteryDrawResult

    def getLotteryUnsortDrawresult(self):
        return self.lotteryUnsortDrawresult

    def getLotteryDrawTime(self):
        return self.lotteryDrawTime