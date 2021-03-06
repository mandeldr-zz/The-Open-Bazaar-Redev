import hashlib
import json
import time
from PIL import Image
from ImageStorage import *

##
# RicardianContract
#     Implements the interface of a Ricardian Contract
#     Will store each state of the contract as it progresses through signing
#
class RicardianContract(object):


    ##
    # Creates a Ricardian Contract from the specified contract data,
    # using the user data specified in seller_settings
    #     @param contract_dict: data about the contract
    #     @param seller_settings: settings for contract creator
    def __init__(self, contract_dict, seller_settings, guid, pubkey):
        self.contract = dict()
        ##
        # Add the metadata components to the contract
        self.contract['metadata'] = dict(expiry=contract_dict['expiry'],
                                         date=time.strftime("%Y:%m:%d:%H:%M:%S"))

        ##
        # Add the id components to the contract
        self.contract['id'] = {}
        self.contract['id']['seller'] = seller_settings
        self.contract['id']['seller']['guid'] = guid
        self.contract['id']['seller']['pubkey'] = pubkey
        self.contract['id']['buyer'] = dict()
        self.contract['id']['notary'] = dict()

        ##
        # Add the trade components to the contract
        self.contract['trade'] = dict(price=contract_dict['price'],
                                      name=contract_dict['item_name'],
                                      description=contract_dict['description'])

        ##
        # Convert keywords to a list
        key_list = contract_dict['keywords'].split(',')
        for count, key in enumerate(key_list):
            key_list[count] = key.strip()
        self.contract['trade']['keywords'] = key_list

        ##
        # Convert image from path to pickle-able object
        self.contract['trade']['images'] = list()
        for image_path in contract_dict['images']:
            self.contract['trade']['images'].append(ImageStorage(str(image_path)))

        ##
        # Add the ledger to the contract
        self.contract['ledger'] = dict(buyer=dict(),
                                       seller=dict())



    ##
    # Sign the contract
    #     @param seller_gpg: GPG object for the seller
    def sign(self, seller_gpg):
        signature = seller_gpg.sign(str(self.contract_hash()))
        self.contract['ledger']['seller'] = signature

    ##
    # Sign the contract for purchase
    #     @param buyer_gpg: GPG object for the buyer
    def purchase(self, buyer_gpg):
        signature = buyer_gpg.sign(str(self.contract_hash()))
        self.contract['ledger']['buyer'] = signature

    ##
    # Returns the specified module from this contract instance
    def get_module(self, module):
        return self.contract[module]

    ##
    # Return a hash of the contract
    def contract_hash(self):
        return self.__hash__()

    ##
    # Returns raw dict data for contract
    # TODO improve this
    def get_dict(self):
        return self.contract

    ##
    # Returns list of keywords associated with this contract
    def get_keywords(self):
        return self.get_module('trade')['keywords']

    ##
    # Returns the itemname for this contract
    def get_itemname(self):
        return self.get_module('trade')['name']

    ##
    # Returns the seller name
    def get_sellername(self):
        return self.get_module('id')['seller']['nickname']