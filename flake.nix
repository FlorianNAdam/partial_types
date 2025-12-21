{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = nixpkgs.lib.systems.flakeExposed;

      perSystem =
        {
          config,
          self',
          inputs',
          pkgs,
          system,
          lib,
          ...
        }:
        let
          partial-types = import ./default.nix { inherit pkgs; };

          mypy-python = pkgs.python3.withPackages (
            ps: with ps; [
              mypy
              pydantic
            ]
          );

          custom-mypy = pkgs.stdenv.mkDerivation {
            pname = "custom-mypy";
            version = pkgs.mypy.version;

            src = ./.;

            buildInputs = [
              mypy-python
            ];

            installPhase = ''
              mkdir -p $out/bin
              ln -s ${mypy-python}/bin/mypy $out/bin/custom-mypy
            '';
          };
        in
        {
          packages = {
            inherit partial-types custom-mypy;
            default = partial-types;
          };

          devenv.shells.default = {
            packages =
              with pkgs;
              [
                ruff
              ]
              ++ (with python312Packages; [
                jedi-language-server
              ]);

            languages.python = {
              enable = true;
              venv.enable = true;
              uv.enable = true;
            };

            git-hooks.hooks = {
              shellcheck.enable = true;
              black.enable = true;
              isort = {
                enable = true;
                settings.profile = "black";
              };
              flake8 = {
                enable = true;
                settings.extendIgnore = [
                  "E501"
                  "W503"
                  "E203"
                ];
              };
              autoflake = {
                enable = true;
                settings.flags = lib.concatStringsSep " " [
                  "--in-place"
                  "--expand-star-imports"
                  "--remove-duplicate-keys"
                  "--remove-unused-variables"
                  "--remove-all-unused-imports"
                ];
              };
              mypy = {
                enable = true;
                settings = {
                  binPath = "${custom-mypy}/bin/custom-mypy";
                };
              };
              flynt.enable = true;
            };
          };
        };
    };
}
