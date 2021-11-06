package com.csi_homies.byte_a_block.activities

import android.content.Intent
import android.graphics.Typeface
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.WindowInsets
import android.view.WindowManager
import android.widget.Toast
import com.csi_homies.byte_a_block.utils.Constants
import kotlinx.android.synthetic.main.activity_intro.*
import kotlinx.android.synthetic.main.activity_sign_in.*

class IntroActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_intro)

        // FLAG_FULLSCREEN got deprecated after R
        @Suppress("DEPRECATION")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            window.insetsController?.hide(WindowInsets.Type.statusBars())
        } else {
            window.setFlags(
                WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN
            )
        }

        // This is used to get the file from the assets folder and set it to the title textView.
        val typeface: Typeface =
            Typeface.createFromAsset(assets, "carbon bl.ttf")
        appNameIntroTextView.typeface = typeface

        introSignInButton.setOnClickListener {
            if (isNetworkAvailable(this)) {
                // Launch the sign in screen.
                startActivity(Intent(this@IntroActivity, SignInActivity::class.java))
            } else {
                Toast.makeText(this@IntroActivity,
                    "No Internet Connection Available.",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }

        /*
        We are not implementing signing up on mobile app for 2 reasons:
            1. We don't want to do double work (There is already a sign up page on the Website
            2. Not anyone in the public should be able to download this app and become an investigator
         */
        signUpButton.setOnClickListener {
            if (isNetworkAvailable(this)) {
                val officialSiteURL = Constants.SIGN_UP_URL
                val openSignUpWebPage = Intent(Intent.ACTION_VIEW)
                openSignUpWebPage.data = Uri.parse(officialSiteURL)
                startActivity(openSignUpWebPage)
            } else {
                Toast.makeText(this@IntroActivity,
                    "No Internet Connection Available.",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }
    }
}