import quickfix as fix
import quickfix44 as fix44
import uuid
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

def start_fix_engine():
    global initiator
    settings = fix.SessionSettings("trade.cfg")
    app = Application()
    storeFactory = fix.FileStoreFactory("store")
    logFactory = fix.FileLogFactory("log")

    initiator = fix.SocketInitiator(app, storeFactory, settings, logFactory)
    initiator.start()
    print("FIX engine started.")

def send_order(symbol, quantity, side):
    if not initiator or not initiator.getSessions():
        raise Exception("FIX session not started or not logged in.")

    order = fix44.NewOrderSingle(
        fix.ClOrdID(str(uuid.uuid4())),
        fix.HandlInst('1'),
        fix.Symbol(symbol),
        fix.Side(side),
        fix.TransactTime(datetime.utcnow()),
        fix.OrdType(fix.OrdType_MARKET)
    )
    order.setField(fix.OrderQty(quantity))

    session_id = initiator.getSessions()[0]
    fix.Session.sendToTarget(order, session_id)
    print("Order sent:", order.toString())
