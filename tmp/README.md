The tmp folder is used to store temporary custom payloads produced by the ``main_attacker`` object.

In patricular those payloads are created by the ``winplant``, ``linplant`` and ``exeplant`` methods of the ``Attacker`` class. They are the used to be dispatched on targets machines.

The payloads are stored as ``.py`` files with randomized alphanumeric names.

To erase all temporary files at once, juste run the powershell script ``clean_tmp.ps1``, sotred in [a relative link](src/scripts/clean_tmp.ps1)