# Tildens problem 2
* Namespace: picoctf/18739f24
* ID: tilden-challenge-2
* Type: custom
* Category: Misc
* Points: 10
* Templatable: yes
* MaxUsers: 1

## Description
Here's my echo server... kinda. Anyways there's no way that you can get my flag.

## Details
You can connect to the server with `nc {{server}} {{port}}`.
Oh, and herer is the code {{url_for("challenge.py", "challenge.py")}}

## Hints
* What permissions do you have?
* Where does data get output?
* TOCTOU-ish

## Solution Overview
* Output echo to flag
* Then solve and get real flag

## Attributes
* author: Tilden Jackson
* organization: 18739

