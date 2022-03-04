from apps.core.models import SaasInstance
from django.contrib.auth.models import User
from django.db import connection
import random
from django.db import transaction
from django.conf import settings

class LogicInstances:
    @transaction.atomic
    def create_new_instance(self, hostname, product):
        # generate new password
        new_password = User.objects.make_random_password(length=16)
        # generate the db password
        db_password = User.objects.make_random_password(length=16)

        # find new available identifier
        instance_id_start = settings.INSTANCE_ID_START
        instance_id_end = settings.INSTANCE_ID_END
        startport = settings.PORT_START
        endport = settings.PORT_END
        new_id = random.randrange(instance_id_start, instance_id_end)
        while SaasInstance.objects.filter(identifier=str(new_id), product = product).exists():
          new_id = random.randrange(instance_id_start, instance_id_end)

        # find new available port on that host, independant of the product
        new_port = -1
        last_port = -1
        if product.number_of_ports > 0:
          if SaasInstance.objects.filter(hostname=hostname).exists():
            with connection.cursor() as cursor:
              sql = """SELECT MAX(last_port) FROM `saas_instance` WHERE hostname = %s"""
              cursor.execute(sql, [hostname,])
              port_result = cursor.fetchone()
              if port_result:
                new_port = port_result[0]
          if new_port < startport:
            new_port = startport
          last_port = new_port + product.number_of_ports - 1

        if new_port > endport:
          return False, {}

        # store to database
        instance = SaasInstance.objects.create(
          identifier = str(new_id),
          hostname = hostname,
          product = product,
          first_port = new_port,
          last_port = last_port,
          initial_password = new_password,
          db_password = db_password,
          status = 'in_preparation')

        # return the result
        return True, {'new_id': new_id, 'new_password': new_password, 'db_password': db_password, 'hostname': hostname, 'port': new_port};
