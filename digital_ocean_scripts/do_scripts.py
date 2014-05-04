# Digital Ocean Functions

import requests
import os

# For this to work, the digitalocean DO_API_KEY, DO_CLIENT_KEY and DO_DEFAULT_SSH_KEY
# should be set as environmental variables
# linux examples in ~./bashrc
# export DO_API_KEY=###########################
# export DO_CLIENT_KEY=#########################
# export DO_DEFAULT_SSH_KEY=#########################

# Client Code and Api Code are both provided on the digital ocean

baseDOurl = 'https://api.digitalocean.com'


def get_env_variable(var_name):
    """" Try and get the environmental variable """
    try:
        return os.environ[var_name]
    except:
        error_msg = "Set environmental variable %s" % var_name
        print error_msg


clientIdVar = get_env_variable('DO_CLIENT_KEY')
apiVar = get_env_variable('DO_API_KEY')
defaultSSHkey = get_env_variable('DO_DEFAULT_SSH_KEY')

doPayload = {'client_id': clientIdVar,
             'api_key': apiVar
             }

# Information about the currently running droplets
# GET
# https://api.digitalocean.com/droplets/?client_id=[client_id]&api_key=[api_key]


def dropletInfo():

    infoURL = baseDOurl + '/droplets/'

    try:
        get_response = requests.get(url=infoURL, params=doPayload)
        try:
            activeDroplets = get_response.json()
        except:
            print('Unable to convert activeDroplets to json()')
        # print('Connection Success! \nStatus Code: ' + str(get_response.status_code))
        print activeDroplets

    except:
        print('Connection Error / Status Code')
              #  + str(get_response.status_code))

    try:
        dDroplets = activeDroplets.get('droplets')
        print('\n' + str(len(dDroplets)) + ' Droplet(s) Currently Running\n')
        for d in dDroplets:
            print ('Droplet ID: ' + str(d['id'])
                   + '\nName: ' + str(d['name'])
                   + '\nIP: ' + str(d['ip_address'])
                   + '\nStatus: ' + str(d['status']) + ' \n')
    except:
        print('error getting droplets')
    print infoURL

# Create A Droplet
# First determine what your image will be
# GET
# https://api.digitalocean.com/images/[image_id_or_slug]/?client_id=[client_id]&api_key=[api_key]


def getImageInfo(image_id):
    # 3101045  = 'Ubuntu 12.04.4 x64'#'Ubuntu 12.04.4 x64'
    getThisImage = image_id
    showImgURL = baseDOurl + '/images/' + str(getThisImage) + '/'
    showImages = requests.get(showImgURL, params=doPayload)
    print showImages.json()

# Get the available SSH Key numbers
# GET
# https://api.digitalocean.com/ssh_keys/?client_id=[client_id]&api_key=[api_key]


def getSSHKeys():
    sshURL = baseDOurl + '/ssh_keys/'
    sshKeys = requests.get(sshURL, params=doPayload)
    print sshKeys.json()

# Actually create the droplet
# GET
# https://api.digitalocean.com/droplets/new?client_id=[client_id]&api_key=[api_key]&name=[droplet_name]&size_id=[size_id]&image_id=[image_id]&region_id=[region_id]&ssh_key_ids=[ssh_key_id1],[ssh_key_id2]


def createDroplet(new_droplet_name):
    newDropletName = new_droplet_name
    newDropletSize = 66
    newDropletRegion = 4
    newDropletImage = 3101045  # 'Ubuntu 12.04.4 x64'
    newDropletSSH = defaultSSHkey

    createPayload = {'client_id': clientIdVar,
                     'api_key': apiVar,
                     'name': newDropletName,
                     'size_id': newDropletSize,
                     'image_id': newDropletImage,
                     'region_id': newDropletRegion,
                     'ssh_key_ids': newDropletSSH}

    createDropletURL = baseDOurl + '/droplets/new'
    newDropletResponse = requests.get(createDropletURL, params=createPayload)
    print newDropletResponse.json()

# Destroy A Droplet
# GET
# https://api.digitalocean.com/droplets/[droplet_id]/destroy/?client_id=[client_id]&api_key=[api_key]


def destroyDroplet(droplet_to_destroy):

    destroyDropletId = droplet_to_destroy
    destroyDropletURL = baseDOurl + '/droplets/' + \
        str(destroyDropletId) + '/destroy/'
    destroyResponse = requests.get(destroyDropletURL, params=doPayload)
    print destroyResponse.json()

# Rebuild the droplet
# GET
# https://api.digitalocean.com/droplets/[droplet_id]/rebuild/?image_id=[image_id]&client_id=[client_id]&api_key=[api_key]


def rebuildDroplet(droplet_to_rebuild):
    rebuildDropletID = droplet_to_rebuild
    rebuildImage = 3101045  # 'Ubuntu 12.04.4 x64'
    rebuildPayload = {'image_id': rebuildImage,
                      'client_id': clientIdVar,
                      'api_key': apiVar,
                      }
    rebuildDropletURL = 'https://api.digitalocean.com/droplets/' + \
        str(rebuildDropletID) + '/rebuild/'
    rebuildResponse = requests.get(rebuildDropletURL, params=rebuildPayload)
    print rebuildResponse.json()
