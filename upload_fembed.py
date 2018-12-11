from tusclient import client

my_client = client.TusClient('http://master.tus.io/files/',
                             headers={'Authorization': 'Basic xxyyZZAAbbCC='})
my_client.set_headers({'HEADER_NAME': 'HEADER_VALUE'})
