require 'test_helper'

class TopControllerTest < ActionController::TestCase
  test "should get index" do
    get :index
    assert_response :success
  end

  test "should get refresh" do
    get :refresh
    assert_response :success
  end

  test "should get view" do
    get :view
    assert_response :success
  end

  test "should get print" do
    get :print
    assert_response :success
  end

end
