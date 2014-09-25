#ShockShell - Bashing on Bash
##Version 0.1

[Description]
Shockshell is an "interactive" shell using the remote command injection vulnerability disclosed in the Bash shell in September of 2014 (CVE-2014-6271,CVE-2014-7169). The long and the short of this is that Bash fails to properly handle specific input when environment variables are being set based on untrusted input. Several attack vectors exist, but Shockshell is really just concerned with vulnerable CGIs (written in Bash only, obviously) as well as any other Web scripts that either are directly or have specific hand-offs to Bash scripts or direct shell commands. As this tool is being written, we are still in the early stages of determining exactly where and how this vulnerability is going to bite us, so I expect several novel attack vectors to arise in the next few weeks/months. 

[How it works]
Shockshell isn't directly designed to allow a pentester to drop a remote shell on a web server, though that is definitely possible using this tool as a delivery and execution vector. Shockshell is a tool to mimic the cmd/result of a normal shell. This can allow a tester the ability to recon a server to determine the best method of gaining shell, reading/discovering local files of a sensitive nature, etc.

Shockshell uses the standard web interface to inject its commands. The injection method is based directly on Robert Grahams' et. al. work for PoC strings, so thanks for all that. Shockshell is simply using a local cURL instance on the target server to make a POST back to an HTTP listener within the Python script. The payload of this POST is the result of the command requested. Obviously, Shockshell relies on several things

* A local install of cURL (wget and other types of support coming soon)
* Outbound HTTP access from the server to the local listener (listener must either be on the general Internet or exposed via NAT, etc.)
* Predictable pathing for the command being run - most instances will not have a $PATH statement so full paths are needed (future version may substitute single commands for their most common full path variants)

[Disclaimer]
This tool is designed for use by penetration testers and system administrators. The standard disclaimers about permissions, etc. apply. 

[Tested On]
So far, this has only been tested on basic mod_cgi's operating under Apache on Debian. I'm currently on vacation and that's all I have access to. I'd appreciate any feedback on how it operates on other environments.

Full error handling is not yet complete. Things may break spectacularly until everything is done.

[Author]
Written by Josh Little (@zombietango)