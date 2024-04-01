from processing.process_main import ProcessingMain
from zappa.asynchronous import task
from authentication.models import User
from nutritional_table.models import NutritionalTable

@task
def async_process_data(user_id, nutritional_table_id, new_response):
    user = User.objects.filter(id=user_id).first()
    nutritional_table = NutritionalTable.objects.filter(id=nutritional_table_id).first()
    ProcessingMain(user, nutritional_table, new_response).run()