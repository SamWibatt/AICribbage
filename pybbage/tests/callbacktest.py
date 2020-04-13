# test to see how to make a class that you can register callbacks with

class EventList:
    def __init__(self):
        self.callbacks = []

    def register(self,callback):
        self.callbacks.append(callback)
        return len(self.callbacks) - 1     # return index of newly added callback

    def invoke_callback(self,index,*cbargs,**cbkwargs):
        print("event list about to invoke callback",index)
        print("cbargs are",cbargs)
        print("cbkwargs are",cbkwargs)
        self.callbacks[index](*cbargs,**cbkwargs)
        # if cbargs is not None:
        #     self.callbacks[index](*cbargs)
        # else:
        #     self.callbacks[index]()

class Mainclass:
    def __init__(self):
        self.evlist = EventList()

    def run(self):
        print("About to register")
        mcbindex = self.evlist.register(self.mycallback)
        print("callback index is",mcbindex)
        print("call with no message:")
        self.evlist.invoke_callback(mcbindex)
        print("call with positional arg message:")
        self.evlist.invoke_callback(mcbindex,"Chunklebunkle")
        print("call with keyword arg message:")
        self.evlist.invoke_callback(mcbindex,message = "tligbot")

    def mycallback(self,message = None):
        if message is None:
            print("Hey! Callback here! No message")
        else:
            print("Hey! Callback has message",message)

if __name__ == "__main__":
    mc = Mainclass()
    mc.run()
