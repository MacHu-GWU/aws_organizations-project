graph TD
%% AWS Organization Structure Mermaid Diagram
%% paste the following content to https://mermaid.live/edit to visualize
%% Circle = Organization | Organization Unit
%% Square = AWS Account
N0(("root
(o-789)"))
N1["admin
(111111111111)"]
N2(("Security
(ou-111)"))
N3["sec_login
(222222222222)"]
N4["sec_audit
(333333333333)"]
N5(("Application
(ou-222)"))
N6["devops
(444444444444)"]
N7["app-dev
(555555555555)"]
N8["app-test
(666666666666)"]
N9["app-prod
(777777777777)"]
N0-->N1
N0-->N2
N0-->N5
N2-->N3
N2-->N4
N5-->N6
N5-->N7
N5-->N8
N5-->N9