import quickfix as fix

class FIXApplication(fix.Application):
    def onCreate(self, sessionID): pass
    def onLogon(self, sessionID): print(f"Logon: {sessionID}")
    def onLogout(self, sessionID): print(f"Logout: {sessionID}")
    def toAdmin(self, message, sessionID): pass
    def toApp(self, message, sessionID): pass
    def fromAdmin(self, message, sessionID): pass
    def fromApp(self, message, sessionID): print(f"Received: {message}")

    def send_order(self, symbol, quantity, side):
        order = fix.Message()
        order.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
        order.setField(fix.ClOrdID("ORDER123"))
        order.setField(fix.Symbol(symbol))
        order.setField(fix.Side(fix.Side_BUY if side.lower() == "buy" else fix.Side_SELL))
        order.setField(fix.OrdType(fix.OrdType_MARKET))
        order.setField(fix.TransactTime())
        order.setField(fix.OrderQty(float(quantity)))
        fix.Session.sendToTarget(order)

def start_fix_engine():
    settings = fix.SessionSettings("trade.cfg")
    app = FIXApplication()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(app, storeFactory, settings, logFactory)
    initiator.start()
    return app