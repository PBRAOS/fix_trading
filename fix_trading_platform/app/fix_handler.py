import quickfix as fix
#import quickfix44 as fix44
#import uuid
from datetime import datetime

initiator = None  # Will hold the Socket Initiator instance

class Application(fix.Application):
    def onCreate(self, sessionID):
        print("FIX session created:", sessionID)

    def onLogon(self, sessionID):
        print("FIX logon:", sessionID)

    def onLogout(self, sessionID):
        print("FIX logout:", sessionID)

    def toAdmin(self, message, sessionID):
        print("Sending admin message:", message.toString())

    def fromAdmin(self, message, sessionID):
        print("Received admin message:", message.toString())

    def toApp(self, message, sessionID):
        print("Sent app message:", message.toString())

    def fromApp(self, message, sessionID):
        print("Received app message:", message.toString())
        self.onMessage(message, sessionID)

    def onMessage(self, message, sessionID):
        print("Application message received.")

    def send_order(self):
        if not initiator or not initiator.getSessions():
            raise Exception("FIX session not started or not logged in.")

        """Request sample new order single"""
        message = fix.Message()
        header = message.getHeader()

        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))  # 39 = D

        message.setField(fix.ClOrdID(self.genClOrdID()))  # 11 = Unique Sequence Number
        message.setField(fix.Side(fix.Side_BUY))  # 43 = 1 BUY
        message.setField(fix.Symbol("MSFT"))  # 55 = MSFT
        message.setField(fix.OrderQty(10000))  # 38 = 1000
        message.setField(fix.Price(100))
        message.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40=2 Limit Order
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))  # 21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))
        trstime = fix.TransactTime()
        trstime.setString(datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)

        fix.Session.sendToTarget(message, self.sessionID)

def start_fix_engine():
    global initiator
    settings = fix.SessionSettings("trade.cfg")
    app = Application()
    storeFactory = fix.FileStoreFactory("store")
    logFactory = fix.FileLogFactory("log")

    # Setup the Socket initiator.
    initiator = fix.SocketInitiator(app, storeFactory, settings, logFactory)
    initiator.start()
    print("FIX engine started.")

