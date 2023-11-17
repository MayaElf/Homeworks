*** Settings ***
Library  SeleniumLibrary
Library  Collections

*** Variables ***
# Settings
${browser}  chrome
${url}  https://www.demoblaze.com/
${login}    snowfallslow@gmail.com
${password}     1qa2ws3ed
# Home Page
${HOME_PAGE_LOGIN_BUTTON}     id:login2
${MONITOR_ELEMENT}    xpath=//*[contains(text(),'monitor')]
${PRICES_XPATH}    xpath=//*[contains(text(),'$')]
# Log In Dialog Window
${USER_NAME_INPUT}   id:loginusername
# Product Page
${PRODUCT_NAME}    xpath=//div[@id='tbodyid']/h2[@class='name']
${PRODUCT_PRICE}    css=#tbodyid .price-container
${ADD_TO_CART}  xpath=//div[@id='tbodyid']//a[contains(text(),'Add to cart')]
${CART_BUTTON}  xpath=//div[@class='navbar-collapse']//li/a[@id='cartur']
# Cart Page
${PRODUCT_NAME_IN_CART}    css=#tbodyid td:nth-of-type(2)
${PRODUCT_PRICE_IN_CART}    css=#tbodyid td:nth-of-type(3)

*** Keywords ***
LoginPreconditions
    Open Browser    ${url}    ${browser}
    ClickLogInButton
    ValidateLoginAndPasswordFieldsArePresented
    LoginToApplication
    CheckLogOutButtonIsVisible

ClickLogInButton
    Wait Until Element Is Visible  ${HOME_PAGE_LOGIN_BUTTON}
    click element    ${HOME_PAGE_LOGIN_BUTTON}

ValidateLoginAndPasswordFieldsArePresented
    Wait Until Element Is Visible  ${USER_NAME_INPUT}
    element should be visible  ${USER_NAME_INPUT}
    element should be visible  id:loginpassword

LoginToApplication
    Wait Until Element Is Visible  ${USER_NAME_INPUT}
    input text  ${USER_NAME_INPUT}    ${login}
    Input Text    id:loginpassword    ${password}
    Click Element    xpath://div[@class='modal-footer']/button[text()='Log in']

checkLogOutButtonIsVisible
    Wait Until Element Is Visible  id:logout2
    element should be visible  id:logout2

validateWelcomeMessageText
    [Arguments]     ${message}
    element should contain  id:nameofuser   ${message}

ClickOnCategory
    reload page
    [Arguments]     ${category}
    Wait Until Element Is Visible  xpath://div[@class='list-group']/a[text()='${category}']
    click element  xpath://div[@class='list-group']/a[text()='${category}']

ClickOnTheProductWithTheHighestPrice
    Wait Until Page Contains Element    ${MONITOR_ELEMENT}
    ${prices}=    Get WebElements    ${PRICES_XPATH}
    ${prices_list}=    Create List
    FOR    ${price}    IN    @{prices}
        Append To List    ${prices_list}    ${price.text}
    END
    ${max_price}=    Set Variable    ${prices_list}[${prices_list.index(max(${prices_list}))}]

    ${any_price_selector}=    Set Variable    //*[contains(text(),'$')]/preceding-sibling::*[@class='card-title']/a
    ${max_price_selector}=    Set Variable    ${any_price_selector.replace('$', '${max_price}')}

    Click Element    xpath=${max_price_selector}

ValidateProductPageOpened
    reload page
    [Arguments]     ${expected_name}     ${expected_price}
    wait until element is visible  ${PRODUCT_NAME}
    element text should be  ${PRODUCT_NAME}     ${expected_name}
    element should contain   ${PRODUCT_PRICE}    ${expected_price}

ClickOnAddToCartButton
    click element  ${ADD_TO_CART}

ClickOnCartButton
    click element   ${CART_BUTTON}

ValidateProductIsSuccessfullyAddedToCart
    [Arguments]     ${expected_name_in_cart}     ${expected_price_in_cart}
    wait until element is visible  ${PRODUCT_NAME_IN_CART}
    element text should be  ${PRODUCT_NAME_IN_CART}     ${expected_name_in_cart}
    element text should be  ${PRODUCT_PRICE_IN_CART}    ${expected_price_in_cart}
