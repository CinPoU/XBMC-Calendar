# If the dir exists with the requested name, simply return it
 
__all__ = [
    # public names
    "XBMC_IS_HOME",
    "SPECIAL_XBMC_DIR",
    "SPECIAL_HOME_DIR",
    "SPECIAL_TEMP_DIR",
    "SPECIAL_PROFILE_DIR",
    "SPECIAL_MASTERPROFILE_DIR",
    "SPECIAL_XBMC_HOME",
    "SPECIAL_SCRIPT_DATA",
    ]
 
 
import os
import sys
from xbmc import translatePath
from xbmcaddon import Addon

__addonID__      = "plugin.program.marmiton"
__settings__     = Addon(id='__addonID__')
ROOTDIR = __settings__.getAddonInfo('path') 
 
PLATFORM_MAC = os.environ.get( "OS", "" ).lower() == "os x"
 
 
try: scriptname = sys.modules[ "__main__" ].__script__
except: scriptname = os.path.basename( ROOTDIR )
 
 
SPECIAL_XBMC_DIR = translatePath( "special://xbmc/" )
if PLATFORM_MAC or not os.path.isdir( SPECIAL_XBMC_DIR  ): SPECIAL_XBMC_DIR = translatePath( "Q:\\" )
 
SPECIAL_HOME_DIR = translatePath( "special://home/" )
if PLATFORM_MAC or not os.path.isdir( SPECIAL_HOME_DIR  ): SPECIAL_HOME_DIR = translatePath( "U:\\" )
 
SPECIAL_TEMP_DIR = translatePath( "special://temp/" )
if PLATFORM_MAC or not os.path.isdir( SPECIAL_TEMP_DIR  ): SPECIAL_TEMP_DIR = translatePath( "Z:\\" )
 
SPECIAL_PROFILE_DIR = translatePath( "special://profile/" )
if PLATFORM_MAC or not os.path.isdir( SPECIAL_PROFILE_DIR  ): SPECIAL_PROFILE_DIR = translatePath( "P:\\" )
 
SPECIAL_MASTERPROFILE_DIR = translatePath( "special://masterprofile/" )
if PLATFORM_MAC or not os.path.isdir( SPECIAL_MASTERPROFILE_DIR  ): SPECIAL_MASTERPROFILE_DIR = translatePath( "T:\\" )
 
SPECIAL_XBMC_HOME = ( SPECIAL_HOME_DIR, SPECIAL_XBMC_DIR )[ ( os.environ.get( "OS", "xbox" ).lower() == "xbox" ) ]
 
XBMC_IS_HOME = SPECIAL_HOME_DIR == SPECIAL_XBMC_DIR
 
SPECIAL_SCRIPT_DATA = os.path.join( SPECIAL_PROFILE_DIR, "addon_data", scriptname )
if not os.path.isdir( SPECIAL_SCRIPT_DATA ): os.makedirs( SPECIAL_SCRIPT_DATA )
