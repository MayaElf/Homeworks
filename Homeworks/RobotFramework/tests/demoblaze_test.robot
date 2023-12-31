#https://www.demoblaze.com/ - demo site to test
#https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html Robot Framework documentation
#https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html SeleniumLibrary documentation
#
#HW: Automate testcases using RF and seleniumLibrary
#
#1.
#precondition: User is registered
#step 1: click login button
#  expected result: login and password fields are presented
#step 2 set up login and password and click login button
#  expected result: Log out button is presented;  Welcome {username} message is presented
#
#2.
#precondition: User is registered
#step 1: Click on Monitors category
#step 2: Click on the product with the highest price on the page
#  expected result: product's page with {product_name} and {product_price} is open
#step 3: Click on Add to cart button
#step 4: Click on Cart button
#  expected result: product is successfully added to cart; {product_name} and {product_price} are presented
#
#add listener that will make screenshots after executing every keyword with tag 'screenshot' (optional)

*** Settings ***
Library  SeleniumLibrary
Resource  ../resources/resources.robot
Test Setup  Open Browser    ${url}    ${browser}
Test Teardown   Close Browser


*** Test Cases ***
LoginTest
    ClickLogInButton
    ValidateLoginAndPasswordFieldsArePresented
    LoginToApplication
    CheckLogOutButtonIsVisible
    ValidateWelcomeMessageText  Welcome ${login}

AddToCartTest
    [Setup]    LoginPreconditions
    ClickOnCategory     Monitors
    ClickOnTheProductWithTheHighestPrice
    ValidateProductPageOpened   Apple monitor 24  $400
    ClickOnAddToCartButton
    ClickOnCartButton
    ValidateProductIsSuccessfullyAddedToCart       Apple monitor 24  400
