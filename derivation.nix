{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
    name = "cli password manager";
    version = "1.0";
    propagatedBuildInputs = [ mysql-connector typer inquirer ];
    src = ./.;
}
