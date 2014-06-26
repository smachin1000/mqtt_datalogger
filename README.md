mqtt_datalogger
===============

Sample data logging application using MQTT.  This code consists of two Python programs.  An MQTT client measures various parameters about the local system, then packages them into a data frame using Capn Proto, then publishes that data to an MQTT channel.  A corresponding MQTT subscriber program reads data from the channel.

The run this code you need to install the paho-mqtt Python package.  To use the Capn Proto serialization format you need to follow the instructions at https://github.com/jparyani/pycapnp to install the Python Capn Proto software.

To run the example, execute mqtt_client.py on one Linux machine, then montior the results by running mqtt_subscriber.py on another machine.
