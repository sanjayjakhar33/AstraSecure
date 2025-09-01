"""
Network scanning service using Nmap
"""
import subprocess
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NetworkScanner:
    """Network vulnerability scanner using Nmap"""
    
    def __init__(self):
        self.scan_techniques = {
            "basic": ["-sS", "-O", "-sV"],  # SYN scan, OS detection, version detection
            "comprehensive": ["-sS", "-sU", "-O", "-sV", "-sC", "--script=vuln"],
            "quick": ["-sS", "-T4", "--top-ports", "1000"],
            "stealth": ["-sS", "-T1", "-f"]
        }
    
    def scan_target(
        self, 
        target: str, 
        scan_type: str = "basic",
        custom_options: List[str] = None
    ) -> Dict[str, Any]:
        """
        Perform network scan on target
        
        Args:
            target: IP address, hostname, or CIDR range
            scan_type: Type of scan (basic, comprehensive, quick, stealth)
            custom_options: Custom nmap options
            
        Returns:
            Scan results as dictionary
        """
        try:
            # Build nmap command
            cmd = ["nmap"]
            
            if custom_options:
                cmd.extend(custom_options)
            else:
                cmd.extend(self.scan_techniques.get(scan_type, self.scan_techniques["basic"]))
            
            # Add output format and target
            cmd.extend(["-oX", "-", target])  # XML output to stdout
            
            logger.info(f"Starting scan: {' '.join(cmd)}")
            
            # Execute scan
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise Exception(f"Nmap scan failed: {result.stderr}")
            
            # Parse XML output (simplified)
            scan_data = self._parse_nmap_output(result.stdout)
            
            return {
                "status": "completed",
                "target": target,
                "scan_type": scan_type,
                "timestamp": datetime.utcnow().isoformat(),
                "raw_output": result.stdout,
                "parsed_data": scan_data,
                "vulnerabilities": self._extract_vulnerabilities(scan_data)
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"Scan timeout for target: {target}")
            return {
                "status": "timeout",
                "target": target,
                "error": "Scan timed out after 5 minutes"
            }
        except Exception as e:
            logger.error(f"Scan error for target {target}: {str(e)}")
            return {
                "status": "error",
                "target": target,
                "error": str(e)
            }
    
    def _parse_nmap_output(self, xml_output: str) -> Dict[str, Any]:
        """
        Parse Nmap XML output (simplified version)
        In production, use python-nmap or xml.etree.ElementTree
        """
        # This is a simplified parser - in production use proper XML parsing
        parsed_data = {
            "hosts": [],
            "scan_stats": {},
            "services": []
        }
        
        # Extract basic information from XML (simplified)
        lines = xml_output.split('\n')
        current_host = None
        
        for line in lines:
            line = line.strip()
            
            if 'address addr=' in line:
                # Extract IP address
                start = line.find('addr="') + 6
                end = line.find('"', start)
                if start > 5 and end > start:
                    current_host = {
                        "ip": line[start:end],
                        "ports": [],
                        "os": "unknown"
                    }
            
            elif 'port protocol=' in line and current_host:
                # Extract port information
                if 'state="open"' in line:
                    port_start = line.find('portid="') + 8
                    port_end = line.find('"', port_start)
                    if port_start > 7 and port_end > port_start:
                        port = line[port_start:port_end]
                        current_host["ports"].append({
                            "port": port,
                            "state": "open",
                            "service": "unknown"
                        })
            
            elif '</host>' in line and current_host:
                parsed_data["hosts"].append(current_host)
                current_host = None
        
        return parsed_data
    
    def _extract_vulnerabilities(self, scan_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract potential vulnerabilities from scan data
        """
        vulnerabilities = []
        
        for host in scan_data.get("hosts", []):
            ip = host.get("ip", "unknown")
            
            for port_info in host.get("ports", []):
                port = port_info.get("port")
                
                # Example vulnerability checks
                if port == "21":  # FTP
                    vulnerabilities.append({
                        "title": "FTP Service Detected",
                        "description": "FTP service running on port 21 may be vulnerable to various attacks",
                        "severity": "medium",
                        "affected_asset": f"{ip}:{port}",
                        "category": "network",
                        "remediation": "Consider using SFTP or FTPS instead of plain FTP"
                    })
                
                elif port == "23":  # Telnet
                    vulnerabilities.append({
                        "title": "Telnet Service Detected",
                        "description": "Telnet transmits data in clear text and is inherently insecure",
                        "severity": "high",
                        "affected_asset": f"{ip}:{port}",
                        "category": "network",
                        "remediation": "Replace Telnet with SSH for secure remote access"
                    })
                
                elif port == "80":  # HTTP
                    vulnerabilities.append({
                        "title": "Unencrypted HTTP Service",
                        "description": "Web service running without encryption",
                        "severity": "medium",
                        "affected_asset": f"{ip}:{port}",
                        "category": "web_application",
                        "remediation": "Implement HTTPS with valid SSL/TLS certificate"
                    })
        
        return vulnerabilities
    
    def get_scan_profiles(self) -> Dict[str, Dict[str, Any]]:
        """
        Get available scan profiles
        """
        return {
            "basic": {
                "name": "Basic Scan",
                "description": "Standard TCP SYN scan with OS and version detection",
                "duration": "5-15 minutes",
                "aggressiveness": "medium"
            },
            "comprehensive": {
                "name": "Comprehensive Scan", 
                "description": "Full scan including UDP, scripts, and vulnerability detection",
                "duration": "30-60 minutes",
                "aggressiveness": "high"
            },
            "quick": {
                "name": "Quick Scan",
                "description": "Fast scan of top 1000 ports",
                "duration": "1-5 minutes", 
                "aggressiveness": "medium"
            },
            "stealth": {
                "name": "Stealth Scan",
                "description": "Slow, fragmented scan to avoid detection",
                "duration": "20-45 minutes",
                "aggressiveness": "low"
            }
        }


# Create scanner instance
network_scanner = NetworkScanner()