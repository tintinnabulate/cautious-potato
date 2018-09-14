def get_pseudo_pdf_attachment_body():
       return u"""\
       <hr>
       <h4>Booking Terms & Conditions</h4>
       <small>
       <p>Our booking terms and conditions are listed below. Please read these
carefully as they form the basis of the contract between us.</p>
<p><b>I confirm that I have read and accept the booking conditions.</b></p>
<p>Signed............................................................</p>
<p>Date...............................................................</p>
       """        

def get_booking_confirmation_email_body(data_dict):
    return u"""\
            <p><a href=""><img src="cid:image1"></a></p>
            <p>Dear %(first_name)s,<br><br>
            Thank you for choosing us and the lovely %(property)s apartment.</p>

            <p>We are writing to confirm that we have received your booking for %(number_of_nights)d night(s) from %(arrival_date)s to %(departure_date)s.</p>

            <p>Your booking reference is %(booking_reference)s (please use this with all payments made to us).</p>

            <p>Your arrival time can be any time after 3pm but not later than 10pm on %(arrival_date)s. Please let us know your arrival time so we can meet you with the keys. Your checkout time will be anytime before 11am on %(departure_date)s. Please leave the keys in the key bowl in the hall.</p>

            <p>If you have not already done so please can you provide the following information:<br>
            <ol>
              <li>Contact telephone number</li>
              <li>Expected time of arrival</li>
            </ol></p>

            <p>We now require full payment of GBP%(gross)d.</p>

            <p>Please use one of the payment methods below always including your booking reference %(booking_reference)s. As soon as we confirm the payment we will arrange details for your arrival.</p>

            <p>Payment Details:<br>
            <pre>
            UK Bank Transfer (please put you booking reference in the transfer reference)
            
            </pre>
            </p>

            <p>Attached is a copy of our terms and conditions. Please make sure you have read these as they form the basis for the contract between us.</p>
            
            <p>Please do not hesitate to use the contact information below for any further correspondence or questions you may have.</p>
             
            <p>We very much look forward to your arrival here and hope you enjoy your stay with us.</p>
             
            <p>Kind regards,<br><br>
            Foo</p>

            <p><a href=""><img src="cid:image2"></a></p>

            <p>Foo&nbsp;&nbsp;01010 101010</p><br>

            <p>Address1<br>
            Address2<br>
            Address3</p>

            <p><font color="green">Please consider the environment before printing this email</font></p>

            <p><small>This email and its attachments are intended for the addressee only and may be confidential or the subject of legal privilege.  This email cannot be distributed by the receiver to anyone else other than the addressee without the permission of the sender.  If this email and its attachments have come to you by mistake please delete from your hard drive, and please contact us.</small></p>
            """ % data_dict


def get_booking_confirmation_email_no_payment_body(data_dict):
    return u"""\
            <p><a href=""><img src="cid:image1"></a></p>
            <p>Dear %(first_name)s,<br><br>
            Thank you for choosing us and the lovely %(property)s apartment.</p>

            <p>We are writing to confirm that we have received your booking for %(number_of_nights)d night(s) from %(arrival_date)s to %(departure_date)s.</p>

            <p>Your booking reference is %(booking_reference)s.</p>

            <p>Your arrival time can be any time after 3pm but not later than 10pm on %(arrival_date)s. Please let us know your arrival time so we can meet you with the keys. Your checkout time will be anytime before 11am on %(departure_date)s. Please leave the keys in the key bowl in the hall.</p>

            <p>If you have not already done so please can you provide the following information:<br>
            <ol>
              <li>Contact telephone number</li>
              <li>Expected time of arrival</li>
            </ol></p>

            <p>Attached is a copy of our terms and conditions. Please make sure you have read these as they form the basis for the contract between us.</p>
            
            <p>Please do not hesitate to use the contact information below for any further correspondence or questions you may have.</p>
             
            <p>We very much look forward to your arrival here and hope you enjoy your stay with us.</p>
             
            <p>Kind regards,<br><br>
            Foo</p>

            <p><a href=""><img src="cid:image2"></a></p>

            <p><font color="green">Please consider the environment before printing this email</font></p>

            <p><small>This email and its attachments are intended for the addressee only and may be confidential or the subject of legal privilege.  This email cannot be distributed by the receiver to anyone else other than the addressee without the permission of the sender.  If this email and its attachments have come to you by mistake please delete from your hard drive, and please contact us.</small></p>
            """ % data_dict
