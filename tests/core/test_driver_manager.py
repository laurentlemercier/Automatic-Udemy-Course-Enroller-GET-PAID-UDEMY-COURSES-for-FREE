from unittest import mock
import pytest
from udemy_enroller import DriverManager
from udemy_enroller.driver_manager import (
    ALL_VALID_BROWSER_STRINGS,
    VALID_EDGE_STRINGS,
    VALID_FIREFOX_STRINGS,
    VALID_INTERNET_EXPLORER_STRINGS,
    VALID_OPERA_STRINGS,
)

@pytest.mark.parametrize(
    "browser_name",
    [
        ("chrome"),
        ("chromium"),
        ("edge"),
        ("firefox"),
        ("opera"),
        ("internet_explorer"),
        ("tor"),
    ],
    ids=(
        "create driver chrome",
        "create driver chromium",
        "create driver edge",
        "create driver firefox",
        "create driver opera",
        "create driver internet_explorer",
        "unsupported browser",
    ),
)
@mock.patch("udemy_enroller.driver_manager.webdriver")
@mock.patch("udemy_enroller.driver_manager.ChromeDriverManager")
@mock.patch("udemy_enroller.driver_manager.ChromeService")
@mock.patch("udemy_enroller.driver_manager.GeckoDriverManager")
@mock.patch("udemy_enroller.driver_manager.FirefoxService")
@mock.patch("udemy_enroller.driver_manager.EdgeChromiumDriverManager")
@mock.patch("udemy_enroller.driver_manager.EdgeService")
@mock.patch("udemy_enroller.driver_manager.IEDriverManager")
@mock.patch("udemy_enroller.driver_manager.IEService")
# Suppression du patch OperaDriverManager ici car il n'existe plus dans le code source
@mock.patch("udemy_enroller.driver_manager.ChromeType")
def test_driver_manager_init(
    mock_chrome_type,
    mock_ie_service,
    mock_ie_driver_manager,
    mock_edge_service,
    mock_edge_driver_manager,
    mock_firefox_service,
    mock_firefox_driver_manager,
    mock_chrome_service,
    mock_chrome_driver_manager,
    mock_selenium_web_driver,
    browser_name,
):
    try:
        dm = DriverManager(browser_name)
    except ValueError:
        assert browser_name not in ALL_VALID_BROWSER_STRINGS
    else:
        if browser_name in ("chrome",):
            mock_selenium_web_driver.Chrome.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Chrome()
        elif browser_name in ("chromium", "opera"): # Opera utilise maintenant ChromeDriverManager
            mock_selenium_web_driver.Chrome.assert_called()
            assert dm.driver == mock_selenium_web_driver.Chrome()
        elif browser_name in VALID_FIREFOX_STRINGS:
            mock_selenium_web_driver.Firefox.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Firefox()
        elif browser_name in VALID_EDGE_STRINGS:
            mock_selenium_web_driver.Edge.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Edge()
        elif browser_name in VALID_INTERNET_EXPLORER_STRINGS:
            mock_selenium_web_driver.Ie.assert_called_once()
            assert dm.driver == mock_selenium_web_driver.Ie()