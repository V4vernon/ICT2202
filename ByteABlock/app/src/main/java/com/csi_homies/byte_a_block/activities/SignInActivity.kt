package com.csi_homies.byte_a_block.activities

import android.os.Build
import android.os.Bundle
import android.text.TextUtils
import android.view.WindowInsets
import android.view.WindowManager
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_sign_in.*


class SignInActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_in)

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
        setupActionBar()

        signInButton.setOnClickListener {
            // not a . not b . not c == not (a + b + c)
            if (!(TextUtils.isEmpty(userNameEditText.text.toString().trim())
                        || TextUtils.isEmpty(passwordEditText.text.toString()))) {

                showProgressDialog("Logging in...")

                loadCasesInMainActivity(userNameEditText.text.toString().trim(), passwordEditText.text.toString(), this@SignInActivity)

                hideProgressDialog()
            } else
                Toast.makeText(this, "Please fill up all the fields!", Toast.LENGTH_LONG).show()
        }
    }

    // Setting up Bar button on the Action Bar
    private fun setupActionBar() {

        setSupportActionBar(signInActivityToolBar)

        val actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(true)

            // To create this asset: Go File > New > Vector Asset > Select your clip art
            actionBar.setHomeAsUpIndicator(R.drawable.ic_black_color_back_24dp)
        }

        signInActivityToolBar.setNavigationOnClickListener { onBackPressed() }
    }
}