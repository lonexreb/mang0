{
  description = "mang0 — reproducible toolchain for the open AI-native laptop";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };
      in {
        devShells.default = pkgs.mkShell {
          name = "mang0-dev";

          packages = with pkgs; [
            kicad
            platformio-core
            python3
            python3Packages.pytest
            python3Packages.pyserial
            nodejs_22
            nodePackages.pnpm
            gnumake
            git
            ripgrep
            jq
          ] ++ pkgs.lib.optionals pkgs.stdenv.isLinux [
            gcc-arm-embedded
            openocd
          ];

          shellHook = ''
            echo "mang0 dev shell"
            echo "  kicad:       $(kicad --version 2>/dev/null | head -1)"
            echo "  pio:         $(pio --version 2>/dev/null)"
            echo "  node:        $(node --version)"
            echo ""
            echo "common targets:"
            echo "  cd ec && pio run"
            echo "  kicad-cli sch erc motherboard/motherboard.kicad_sch"
            echo "  kicad-cli pcb drc motherboard/motherboard.kicad_pcb"
          '';
        };
      });
}
