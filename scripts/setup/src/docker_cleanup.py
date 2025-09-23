#!/usr/bin/env python3
"""
Docker Cleanup Management for Portfolio System
Automatically cleans up Docker services after use
"""

import subprocess
import time
import sys
import signal
from pathlib import Path
from typing import List, Optional


class DockerCleanupManager:
    """Manages Docker cleanup operations for the portfolio system"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.compose_files = self._discover_compose_files()
        self.cleanup_registered = False

    def _discover_compose_files(self) -> List[Path]:
        """Discover all docker-compose files in setup directory"""
        setup_dir = self.project_root / "setup"
        compose_files = []

        if setup_dir.exists():
            # Base compose file
            base_file = setup_dir / "docker-compose.yml"
            if base_file.exists():
                compose_files.append(base_file)

            # Generated compose file
            generated_file = setup_dir / "generated" / "docker-compose.generated.yml"
            if generated_file.exists():
                compose_files.append(generated_file)

            # Environment-specific overrides
            for env in ["local", "dev", "test", "prod", "release"]:
                env_file = setup_dir / f"docker-compose.{env}.yml"
                if env_file.exists():
                    compose_files.append(env_file)

        return compose_files

    def get_compose_command(self, environment: str = "local") -> List[str]:
        """Build docker-compose command with appropriate files"""
        cmd = ["docker-compose"]

        # Add base compose file
        base_file = self.project_root / "setup" / "docker-compose.yml"
        if base_file.exists():
            cmd.extend(["-f", str(base_file)])

        # Add generated compose file
        generated_file = self.project_root / "setup" / "generated" / "docker-compose.generated.yml"
        if generated_file.exists():
            cmd.extend(["-f", str(generated_file)])

        # Add environment-specific override
        env_file = self.project_root / "setup" / f"docker-compose.{environment}.yml"
        if env_file.exists():
            cmd.extend(["-f", str(env_file)])

        return cmd

    def stop_services(self, environment: str = "local", timeout: int = 30):
        """Stop all running services gracefully"""
        cmd = self.get_compose_command(environment)
        cmd.extend(["stop", "--timeout", str(timeout)])

        print(f"🛑 Stopping services (timeout: {timeout}s)...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                print("✅ Services stopped successfully")
            else:
                print(f"⚠️ Warning during stop: {result.stderr}")
        except subprocess.SubprocessError as e:
            print(f"❌ Error stopping services: {e}")

    def remove_containers(self, environment: str = "local"):
        """Remove all containers"""
        cmd = self.get_compose_command(environment)
        cmd.extend(["rm", "-f"])

        print("🗑️ Removing containers...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                print("✅ Containers removed successfully")
            else:
                print(f"⚠️ Warning during removal: {result.stderr}")
        except subprocess.SubprocessError as e:
            print(f"❌ Error removing containers: {e}")

    def remove_networks(self, environment: str = "local"):
        """Remove custom networks"""
        cmd = self.get_compose_command(environment)
        cmd.extend(["down", "--remove-orphans"])

        print("🌐 Removing networks...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                print("✅ Networks removed successfully")
            else:
                print(f"⚠️ Warning during network removal: {result.stderr}")
        except subprocess.SubprocessError as e:
            print(f"❌ Error removing networks: {e}")

    def cleanup_volumes(self, keep_data: bool = True):
        """Clean up unused volumes (optionally keep data volumes)"""
        print("💾 Cleaning up volumes...")

        if not keep_data:
            # Remove all unused volumes
            try:
                subprocess.run(["docker", "volume", "prune", "-f"],
                             capture_output=True, text=True)
                print("✅ Unused volumes cleaned")
            except subprocess.SubprocessError as e:
                print(f"❌ Error cleaning volumes: {e}")
        else:
            print("ℹ️ Keeping data volumes (use --remove-data to clean all)")

    def cleanup_images(self, remove_all: bool = False):
        """Clean up unused images"""
        print("🗑️ Cleaning up images...")

        try:
            if remove_all:
                # Remove all unused images including tagged ones
                subprocess.run(["docker", "image", "prune", "-a", "-f"],
                             capture_output=True, text=True)
                print("✅ All unused images removed")
            else:
                # Remove only dangling images
                subprocess.run(["docker", "image", "prune", "-f"],
                             capture_output=True, text=True)
                print("✅ Dangling images removed")
        except subprocess.SubprocessError as e:
            print(f"❌ Error cleaning images: {e}")

    def full_cleanup(self, environment: str = "local", keep_data: bool = True,
                    keep_images: bool = True):
        """Perform full cleanup of Docker resources"""
        print(f"🧹 Starting full cleanup for environment: {environment}")
        print("=" * 60)

        # Stop services gracefully
        self.stop_services(environment, timeout=30)
        time.sleep(2)

        # Remove containers
        self.remove_containers(environment)
        time.sleep(1)

        # Remove networks
        self.remove_networks(environment)
        time.sleep(1)

        # Clean volumes (conditionally)
        self.cleanup_volumes(keep_data)
        time.sleep(1)

        # Clean images (conditionally)
        if not keep_images:
            self.cleanup_images(remove_all=False)

        print("=" * 60)
        print("✅ Full cleanup completed!")

    def register_exit_handler(self, environment: str = "local"):
        """Register cleanup to run on script exit"""
        if self.cleanup_registered:
            return

        def cleanup_handler(signum, frame):
            print(f"\n🔄 Received signal {signum}, performing cleanup...")
            self.full_cleanup(environment, keep_data=True, keep_images=True)
            sys.exit(0)

        # Register signal handlers
        signal.signal(signal.SIGINT, cleanup_handler)   # Ctrl+C
        signal.signal(signal.SIGTERM, cleanup_handler)  # Termination

        self.cleanup_registered = True
        print(f"🔧 Cleanup handler registered for environment: {environment}")

    def get_running_services(self) -> List[str]:
        """Get list of currently running services"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "label=com.docker.compose.project=portfolio",
                 "--format", "{{.Names}}"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return [name.strip() for name in result.stdout.split('\n') if name.strip()]
            return []
        except subprocess.SubprocessError:
            return []

    def show_status(self):
        """Show current status of Docker services"""
        running_services = self.get_running_services()

        if running_services:
            print(f"🏃 Running services ({len(running_services)}):")
            for service in running_services:
                print(f"   • {service}")
        else:
            print("💤 No portfolio services currently running")

        # Show resource usage
        try:
            result = subprocess.run(["docker", "system", "df"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("\n📊 Docker resource usage:")
                print(result.stdout)
        except subprocess.SubprocessError:
            pass


def main():
    """Main function for Docker cleanup management"""
    import argparse

    parser = argparse.ArgumentParser(description="Docker cleanup management for Portfolio system")
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--environment', default='local',
                       choices=['local', 'dev', 'test', 'prod', 'release'],
                       help='Environment to clean up')
    parser.add_argument('--action', default='status',
                       choices=['status', 'stop', 'cleanup', 'full-cleanup'],
                       help='Action to perform')
    parser.add_argument('--keep-data', action='store_true', default=True,
                       help='Keep data volumes during cleanup')
    parser.add_argument('--remove-images', action='store_true',
                       help='Remove unused images during cleanup')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout for stopping services')

    args = parser.parse_args()

    # Initialize cleanup manager
    cleanup = DockerCleanupManager(args.project_root)

    if args.action == 'status':
        cleanup.show_status()
    elif args.action == 'stop':
        cleanup.stop_services(args.environment, args.timeout)
    elif args.action == 'cleanup':
        cleanup.remove_containers(args.environment)
        cleanup.remove_networks(args.environment)
    elif args.action == 'full-cleanup':
        cleanup.full_cleanup(
            args.environment,
            keep_data=args.keep_data,
            keep_images=not args.remove_images
        )

    print(f"\n🎯 Docker cleanup action '{args.action}' completed for {args.environment}")


if __name__ == "__main__":
    main()