__author__ = "Cobbin"
from models.alerts.alert import Alert
from common.database import Database

Database.initialize()

alerts_needing_update = Alert.find_pending_update()

for alert in alerts_needing_update:
    print(alert)
    alert.load_item_price()
    alert.send_email_if_price_reached()
    print("Email is sent")
