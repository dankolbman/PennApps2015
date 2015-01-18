# Clever Tind - Dating with cleverbot
# Like everyone, download profiles, start and hold conversations!
# Dan Kolbman 2014

require 'json'
require 'pyro.rb'
require 'watir-webdriver'
require 'fileutils'
require 'cleverbot'
require 'time'

# fb_auth.rb holds four variables that need to be defined:
# $myLogin - the facebook e-mail address for the fb account with tinder
# $myPasswork - the password the fb account
# fb_id - the fb id number of the account
#load 'fb_auth.rb', true

# this will be assigned later, needed to authenticate with tinder
$fb_token = ''

################################################################################
# Actual stuff
# Log us in
if($fb_token == '')
  browser = Watir::Browser.new
  browser.goto 'https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token'
  #browser.text_field(:id => 'email').when_present.set $myLogin
  #browser.text_field(:id => 'pass').when_present.set $myPassword
  browser.button(:name => 'login').wait_while_present

  #puts 'Fetching your Facebook ID...'
  $fb_token = /#access_token=(.*)&expires_in/.match(browser.url).captures[0]

  target = open('fb_token.tmp', 'w')
  target.truncate(0)
  target.write($fb_token)
  target.close
  browser.close
end
