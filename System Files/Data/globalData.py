# data file paths

# generate data strcutures
    # convert json system conf file to dict


    # create or reinitialize program data => zones correspond with number of zones in conf file
        # each zone gets => {"Average Zone Moisture": 0 - 100, "Watering Watch Dog": object, "BD Watch Dog": object}
        # webpage => control logic {"ModeToggleFlag": 0 - 1, "WateringToggleFlags" (initilize array with zero for each zone): []}
        # periodic control logic => webpage {"networkConnectionFlag": , "Zones": {"WateringStatus": ,"Zone Moisture"}} => inhibiting and enable will be set from config file client recieves
        # requested control logic => webpage {"system logs": [], "24 hour samples": [], "available networks": []}
        # system wide variables include
            # networkConnectionFlag
            # UpdateConfigFlag
            # 