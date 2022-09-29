import React from 'react'

// importing css
import './css/TermsConditions.css'

export default function TermsConditions() {
    return (
        <div className='tnc-container'>
            <h3 className="warning">This is a personal project login at your own risk</h3>
            <p>This application will not use any personal information except for your uid, profile details</p>
            <h6 className="portfolio-link" >Application Build by <a style={{
                'text-decoration': 'underline',
                'color': 'var(--sp-green)'
            }} href="https://kalluriabhinandan.web.app/" target="_blank"> Abhinandan Kalluri.</a></h6>
            <p style={{ 'margin': '0' }}>
                The github repository of GroupListen-V2 project is private.<br />
                The github repository of GroupListen is public.<br />
            </p>
        </div>
    )
}
