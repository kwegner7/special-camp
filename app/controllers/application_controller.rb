class ApplicationController < ActionController::Base
    #protect_from_forgery
    #config.threadsafe!
    #http_basic_authenticate_with :name => "special", :password => "camp"

  def index
    puts "Initializing the application"
  end
end
