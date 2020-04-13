# test to see how to make a class that you can register callbacks with
# second version, with arguments sent in the register

class EventList:
    def __init__(self):
        self.callbacks = []

    def register(self,callback,*cbargs,**cbkwargs):
        # so, now we append a list s.t. [0] is the callback function pointer, [1] is args, [2] is kwargs
        self.callbacks.append([callback, cbargs, cbkwargs])
        return len(self.callbacks) - 1     # return index of newly added callback

    def invoke_callback(self,index):
        print("event list about to invoke callback",index)
        cbargs = self.callbacks[index][1]
        print("cbargs are",cbargs)
        cbkwargs = self.callbacks[index][2]
        print("cbkwargs are",cbkwargs)
        self.callbacks[index][0](*cbargs,**cbkwargs)

class Mainclass:
    def __init__(self):
        self.evlist = EventList()

    def run(self):
        print("About to register no-message callback")
        # no arguments
        nomsg_index = self.evlist.register(self.mycallback)
        print("callback index is",nomsg_index)
        print("call with no message:")
        self.evlist.invoke_callback(nomsg_index)

        # with positional arg message
        print("\nAbout to register positional-message callback")
        posmsg_index = self.evlist.register(self.mycallback,"Chiddlezop Chunklebunk")
        print("callback index is",posmsg_index)
        print("call with positional arg message:")
        self.evlist.invoke_callback(posmsg_index)

        # with keyword arg message
        print("\nAbout to register keyword-message callback")
        kwmsg_index = self.evlist.register(self.mycallback,message = "glorp blep tlebdness")
        print("callback index is",kwmsg_index)
        print("call with keyword arg message:")
        self.evlist.invoke_callback(kwmsg_index)

    def mycallback(self,message = None):
        if message is None:
            print("Hey! Callback here! No message")
        else:
            print("Hey! Callback has message",message)

if __name__ == "__main__":
    mc = Mainclass()
    mc.run()
