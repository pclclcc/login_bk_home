## Description
This test is to verify login cathay homepage.
It used snippet-uiautomator and mobly to build the test.
-  mobly: https://github.com/google/mobly
-  snippet-uiautomator: https://github.com/google/snippet-uiautomator

## Requirements
-   Android 8.0+ (SDK 26+)
-   adb (1.0.40+ recommended)
-   Python3.11+

## Installation
pip install snippet-uiautomator
pip install mobly

## Compatibility
Mobly requires python 3.11 or newer.
Mobly tests could run on the following platforms:
-   Ubuntu 14.04+
-   MacOS 10.6+
-   Windows 7+

## Command
Navigate to the root directory.
```shell
python test.py -c sample_config.yml
```
Invoking specific test case:
```shell
python test.py -c sample_config.yml --test_case test_product_intro_subfunction
```
Multiple Test Beds and Default Test Parameters:
```shell
python test.py -c sample_config.yml --test_bed SampleTestBed
```

## Note
Due to the webview compatibility of uiautomator, some code is not workable or unstable.
It is proper to test native app.
