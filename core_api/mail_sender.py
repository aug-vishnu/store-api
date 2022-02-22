from django.core.mail import EmailMultiAlternatives



def forgot_otp_mail(customer, forgot_otp):
    subject, from_email = 'Forgot Password Code - Theni Grocery', 'thenigrocery@gmail.com'
    to = customer.user.email
    text_content = 'Alternative'
    html_content = """\

        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>A Simple Responsive HTML Email</title>
        <style type="text/css">
        body {margin: 0; padding: 0; min-width: 100%!important;}
        img {height: auto;}
        .content {width: 100%; max-width: 600px;}
        .header {padding: 40px 30px 20px 30px;}
        .innerpadding {padding: 30px 30px 30px 30px;}
        .borderbottom {border-bottom: 1px solid #f2eeed;}
        .subhead {font-size: 15px; color: #ffffff; font-family: sans-serif; letter-spacing: 10px;}
        .h1, .h2, .bodycopy {color: #153643; font-family: sans-serif;}
        .h1 {font-size: 33px; line-height: 38px; font-weight: bold;}
        .h2 {padding: 0 0 15px 0; font-size: 24px; line-height: 28px; font-weight: bold;}
        .bodycopy {font-size: 16px; line-height: 22px;}
        .button {text-align: center; font-size: 18px; font-family: sans-serif; font-weight: bold; padding: 0 30px 0 30px;}
        .button a {color: #ffffff; text-decoration: none;}
        .footer {padding: 20px 30px 15px 30px;}
        .footercopy {font-family: sans-serif; font-size: 14px; color: #ffffff;}
        .footercopy a {color: #ffffff; text-decoration: underline;}

        @media only screen and (max-width: 550px), screen and (max-device-width: 550px) {
        body[yahoo] .hide {display: none!important;}
        body[yahoo] .buttonwrapper {background-color: transparent!important;}
        body[yahoo] .button {padding: 0px!important;}
        body[yahoo] .button a {background-color: #e05443; padding: 15px 15px 13px!important;}
        body[yahoo] .unsubscribe {display: block; margin-top: 20px; padding: 10px 50px; background: #2f3942; border-radius: 5px; text-decoration: none!important; font-weight: bold;}
        }
        </style>
        </head>

        <body yahoo bgcolor="#f6f8f1">
        <table width="100%" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0">
        <tr>
        <td>
            <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td bgcolor="#c7d8a7" class="header">
                <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                    <td height="70" style="padding: 0 20px 20px 0;">
                        <img class="fix" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/210284/icon.gif" width="70" height="70" border="0" alt="" />
                    </td>
                    </tr>
                </table>
                <table class="col425" align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 425px;">
                    <tr>
                    <td height="70">
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                            <td class="subhead" style="padding: 0 0 0 3px;">
                            YOUR
                            </td>
                        </tr>
                        <tr>
                            <td class="h1" style="padding: 5px 0 0 0;">
                            Theni Groceries
                            </td>
                        </tr>
                        </table>
                    </td>
                    </tr>
                </table>
                </td>
            </tr>
            <tr>
                <td class="innerpadding borderbottom">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td class="h2">
                        We've received your request
                    </td>
                    </tr>
                    <tr>
                    <td class="bodycopy">
                        Hello """ + str(customer.user.email) + """  Use this code for Your forgot password OTP : <strong>""" + str(forgot_otp) + """</strong>  Happy shopping !!
                    </td>
                    </tr>
                </table>
                </td>
            </tr>


            <tr>
                <td class="footer" bgcolor="#44525f">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td align="center" class="footercopy">
                        &reg; APS Infotech <br/>
                    </td>
                    </tr>
                    <tr>
                    </tr>
                </table>
                </td>
            </tr>
            </table>
            </td>
        </tr>
        </table>
        </body>
        </html>



    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def checkout_mail(customer, otp):
    subject, from_email = 'Order placed sucessfully - Theni Grocery', 'thenigrocery@gmail.com'
    to = customer.user.email
    text_content = 'Alternative'
    html_content = """\

        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>A Simple Responsive HTML Email</title>
        <style type="text/css">
        body {margin: 0; padding: 0; min-width: 100%!important;}
        img {height: auto;}
        .content {width: 100%; max-width: 600px;}
        .header {padding: 40px 30px 20px 30px;}
        .innerpadding {padding: 30px 30px 30px 30px;}
        .borderbottom {border-bottom: 1px solid #f2eeed;}
        .subhead {font-size: 15px; color: #ffffff; font-family: sans-serif; letter-spacing: 10px;}
        .h1, .h2, .bodycopy {color: #153643; font-family: sans-serif;}
        .h1 {font-size: 33px; line-height: 38px; font-weight: bold;}
        .h2 {padding: 0 0 15px 0; font-size: 24px; line-height: 28px; font-weight: bold;}
        .bodycopy {font-size: 16px; line-height: 22px;}
        .button {text-align: center; font-size: 18px; font-family: sans-serif; font-weight: bold; padding: 0 30px 0 30px;}
        .button a {color: #ffffff; text-decoration: none;}
        .footer {padding: 20px 30px 15px 30px;}
        .footercopy {font-family: sans-serif; font-size: 14px; color: #ffffff;}
        .footercopy a {color: #ffffff; text-decoration: underline;}

        @media only screen and (max-width: 550px), screen and (max-device-width: 550px) {
        body[yahoo] .hide {display: none!important;}
        body[yahoo] .buttonwrapper {background-color: transparent!important;}
        body[yahoo] .button {padding: 0px!important;}
        body[yahoo] .button a {background-color: #e05443; padding: 15px 15px 13px!important;}
        body[yahoo] .unsubscribe {display: block; margin-top: 20px; padding: 10px 50px; background: #2f3942; border-radius: 5px; text-decoration: none!important; font-weight: bold;}
        }
        </style>
        </head>

        <body yahoo bgcolor="#f6f8f1">
        <table width="100%" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0">
        <tr>
        <td>
            <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td bgcolor="#c7d8a7" class="header">
                <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                    <td height="70" style="padding: 0 20px 20px 0;">
                        <img class="fix" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/210284/icon.gif" width="70" height="70" border="0" alt="" />
                    </td>
                    </tr>
                </table>
                <table class="col425" align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 425px;">
                    <tr>
                    <td height="70">
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                            <td class="subhead" style="padding: 0 0 0 3px;">
                            YOUR
                            </td>
                        </tr>
                        <tr>
                            <td class="h1" style="padding: 5px 0 0 0;">
                            Theni Groceries
                            </td>
                        </tr>
                        </table>
                    </td>
                    </tr>
                </table>
                </td>
            </tr>
            <tr>
                <td class="innerpadding borderbottom">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td class="h2">
                        We've processing your orders 
                    </td>
                    </tr>
                    <tr>
                    <td class="bodycopy">
                        Hello """ + str(customer.user.email) + """  Use this code for Your Order OTP : <strong>""" + str(otp) + """</strong> Show this to our Representative for futher process Happy shopping !!
                    </td>
                    </tr>
                </table>
                </td>
            </tr>


            <tr>
                <td class="footer" bgcolor="#44525f">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td align="center" class="footercopy">
                        &reg; APS Infotech <br/>
                    </td>
                    </tr>
                    <tr>
                    </tr>
                </table>
                </td>
            </tr>
            </table>
            </td>
        </tr>
        </table>
        </body>
        </html>



    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def order_complete(orders, order_otp):
    subject, from_email = 'Order Delivered sucessfully - Theni Grocery', 'thenigrocery@gmail.com'
    to = orders.user.email
    product_table = put_products(orders)
    # print(product_table)
    text_content = 'Alternative'
    html_content = """\

        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>A Simple Responsive HTML Email</title>
        <style type="text/css">
        	.demo {
                margin-bottom: 20px;
                width: 100%;
		border:1px solid #C0C0C0;
		border-collapse:collapse;
		padding:5px;
        }
        .demo .tl{
            text-align:right;
        }
        .demo th {
		border:1px solid #C0C0C0;
		padding:5px;
		background:#F0F0F0;
        }
        .demo td {
		border:1px solid #C0C0C0;
		padding:5px;
        }
        body {margin: 0; padding: 0; min-width: 100%!important;}
        img {height: auto;}
        .content {width: 100%; max-width: 600px;}
        .header {padding: 40px 30px 20px 30px;}
        .innerpadding {padding: 30px 30px 30px 30px;}
        .borderbottom {border-bottom: 1px solid #f2eeed;}
        .subhead {font-size: 15px; color: #ffffff; font-family: sans-serif; letter-spacing: 10px;}
        .h1, .h2, .bodycopy {color: #153643; font-family: sans-serif;}
        .h1 {font-size: 33px; line-height: 38px; font-weight: bold;}
        .h2 {padding: 0 0 15px 0; font-size: 24px; line-height: 28px; font-weight: bold;}
        .bodycopy {font-size: 16px; line-height: 22px;}
        .button {text-align: center; font-size: 18px; font-family: sans-serif; font-weight: bold; padding: 0 30px 0 30px;}
        .button a {color: #ffffff; text-decoration: none;}
        .footer {padding: 20px 30px 15px 30px;}
        .footercopy {font-family: sans-serif; font-size: 14px; color: #ffffff;}
        .footercopy a {color: #ffffff; text-decoration: underline;}

        @media only screen and (max-width: 550zpx), screen and (max-device-width: 550px) {
        body[yahoo] .hide {display: none!important;}
        body[yahoo] .buttonwrapper {background-color: transparent!important;}
        body[yahoo] .button {padding: 0px!important;}
        body[yahoo] .button a {background-color: #e05443; padding: 15px 15px 13px!important;}
        body[yahoo] .unsubscribe {display: block; margin-top: 20px; padding: 10px 50px; background: #2f3942; border-radius: 5px; text-decoration: none!important; font-weight: bold;}
        }
        </style>
        </head>

        <body yahoo bgcolor="#f6f8f1">
        <table width="100%" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0">
        <tr>
        <td>
            <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td bgcolor="#c7d8a7" class="header">
                <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">
                    <tr>
                    <td height="70" style="padding: 0 20px 20px 0;">
                        <img class="fix" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/210284/icon.gif" width="70" height="70" border="0" alt="" />
                    </td>
                    </tr>
                </table>
                <table class="col425" align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 425px;">
                    <tr>
                    <td height="70">
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                            <td class="subhead" style="padding: 0 0 0 3px;">
                            YOUR
                            </td>
                        </tr>
                        <tr>
                            <td class="h1" style="padding: 5px 0 0 0;">
                            Theni Groceries
                            </td>
                        </tr>
                        </table>
                    </td>
                    </tr>
                </table>
                </td>
            </tr>
            <tr>
                <td class="innerpadding borderbottom">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td class="h2">
                        We've delivered your products safely to your hands
                    </td>
                    </tr>
                    <tr>
                    <td class="bodycopy">
                        Hello """ + str(orders.user.email) + """  Thanks for choosing us Happy shopping !!
                    </td>
                    </tr>
                </table>
                </td>
            </tr>
            

            <tr>
                """ + product_table + """
            </tr>

            
            <tr>
                <td class="footer" bgcolor="#44525f">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                    <td align="center" class="footercopy">
                        &reg; APS Infotech <br/>
                    </td>
                    </tr>
                    <tr>
                    </tr>
                </table>
                </td>
            </tr>
            </table>
            </td>
        </tr>
        </table>
        </body>
        </html>



    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, ['vishnuprabhu.bvk@gmail.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def put_products(orders):
    product_table = '''<table class="demo">
	<thead>
        <tr>
            <th>Sl.No</th>
            <th>Product Name</th>
            <th>Qty</th>
            <th>Price</th>
            <th>GST</th>
            <th>Price + GST</th> 
        </tr>	
    </thead>
    <tbody>''' 
        
    for o in range (0,len(orders.order_items.all())):
        
        product_row = '''	
        <tr>
            <td>'''+ str(o+1) +'''</td>
            <td>'''+ str(orders.order_items.all()[o].product.product_name) +'''</td>
            <td class="tl">'''+ str(orders.order_items.all()[o].quantity) +'''</td>
            <td class="tl">'''+ str(orders.order_items.all()[o].product.product_current_price ) +'''</td>
            <td class="tl">'''+ str(orders.order_items.all()[o].product.product_gst) +'''</td>
            <td class="tl">'''+ str(orders.order_items.all()[o].order_item_price) +'''</td>
        </tr> '''

        product_table = product_table + product_row
        product_row = ''




    product_table += '''<tr>
                <td class="tl" colspan="5">&nbsp;Total :</td>
                <td class="tl" colspan="1">&nbsp; ''' + str(orders.order_price) + ''' </td>
            </tr>
            <tbody>
        </table>'''
    return product_table        


