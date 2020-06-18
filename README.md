The following values should be set in charts/hello-world/values.yaml before running hello world helm <br/>
1)	configMap.qidoURL<br/>
2)	configMap.workflowURL<br/>
3)	configMap.imagingURL<br/>
4)	configMap.imagingHost<br/>

Example/Default:<br/>
configMap:<br/>
  qidoURL: "http://a0441b1b022cf4515907980b3c122a4c-976928728.us-east-1.elb.amazonaws.com:30043" <br/>
  workflowURL: "http://a06b15241bc9d434fb6ec33824587190-1479194273.us-east-1.elb.amazonaws.com:8080" <br/>
  imagingURL: "http://aecdc88cda9db4f9baa68fcaa100595b-1589018792.us-east-1.elb.amazonaws.com:4000"<br/>
  imagingHost: "a4aef5d76c05247ffbdd7f04471bc0bd-25671258.us-east-1.elb.amazonaws.com:8080" <br/>
