#!/usr/bin/env python3

from TrainerModule import print_channel_model_pars
import h2o
from optparse import OptionParser

if __name__ == '__main__':
    oparser = OptionParser()
    oparser.add_option("--model-conf-name", action="store",
                       type="string", dest="conf_name")
    oparser.add_option("--dpid", action="store", type="int", dest="dpid")

    (options, args) = oparser.parse_args()

    conf_name=options.conf_name
    dpid = options.dpid

    print(f"conf_name {conf_name}")
    print(f"dpid {dpid}")

    h2o.init()

    print_channel_model_pars.print_pars(conf_name,dpid)
   
