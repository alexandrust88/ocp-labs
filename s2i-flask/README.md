Simple Flask application to demonstrate S2I builds.
Includes an endpoint `/invalidate` to make application seem unhealthy in order to demonstrate built-in self healing capabilities in OpenShift.

Includes version and basic environment-based feature toggle to demonstrate various deployment strategies in OpenShift.

``oc apply -R -f cfg/``
