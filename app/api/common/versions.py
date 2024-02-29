from packaging import version

from fastapi import HTTPException, status


MIN_CLIENT_VERSION = "2.1.0"


class VersionConstroller:
    """Controller class that handles version in the headers."""

    def get_parsed_version_format(self, version_header: str) -> version.Version:
        """Check if string in header is a valid version format."""

        try:
            return version.parse(version_header)
        except version.InvalidVersion:

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Header app-version '{version_header}' is not valid."
            )

    def is_valid_version(self, version_header: str):
        """Check if valid version is lower or equal than version in the input."""

        version_header = self.get_parsed_version_format(version_header)

        if not version.parse(MIN_CLIENT_VERSION) <= version_header:
            validation_error = "Header app-version '{}' is lower than {}."

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=validation_error.format(
                    version_header, MIN_CLIENT_VERSION)
            )
