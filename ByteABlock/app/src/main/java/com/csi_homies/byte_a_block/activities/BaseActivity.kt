package com.csi_homies.byte_a_block.activities

import android.app.Dialog
import android.content.Context
import android.content.Intent
import android.content.Intent.FLAG_ACTIVITY_CLEAR_TASK
import android.content.Intent.FLAG_ACTIVITY_NEW_TASK
import android.content.SharedPreferences
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.csi_homies.byte_a_block.adapters.CaseListAdapter
import com.csi_homies.byte_a_block.utils.Constants
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import com.csi_homies.byte_a_block.models.basic_case_info_response.Case
import com.csi_homies.byte_a_block.network.BasicCaseInfoGet
import com.google.android.material.snackbar.Snackbar
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_sign_in.*
import kotlinx.android.synthetic.main.dialog_progress.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.text.SimpleDateFormat
import java.util.*
import kotlin.collections.ArrayList

/*
This activity is only used for all the other activities to inherit from so that we would not need to
reimplement things over all the other activities we have
 */
open class BaseActivity : AppCompatActivity() {

    private lateinit var mProgressDialog: Dialog

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    fun loadCasesInMainActivity(username: String, password: String, context: Context){
        if(isNetworkAvailable(context)){
            val retrofit: Retrofit = Retrofit.Builder()
                .baseUrl(Constants.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

            val service: BasicCaseInfoGet = retrofit.create<BasicCaseInfoGet>(BasicCaseInfoGet::class.java)

            val listCall: Call<BasicCaseInfoResponse> = service.getBasicCaseInfo(username, password)

            // runs the request on a background thread, and runs the callback on the current thread.
            // enqueue is asynchronous, execute() is synchronous
            listCall.enqueue(object: Callback<BasicCaseInfoResponse> {
                override fun onResponse(
                    call: Call<BasicCaseInfoResponse>,
                    response: Response<BasicCaseInfoResponse>
                ) {
                    if (response.isSuccessful){
                        val basicCaseInfoList: BasicCaseInfoResponse? = response.body()

                        if (context is SignInActivity){
                            storeUserNameAndPassword(username, password)
                            val i = Intent(context, MainActivity::class.java)
                            i.putExtra(Constants.CASE_INFO_ID, Gson().toJson(basicCaseInfoList))
                            i.addFlags(FLAG_ACTIVITY_CLEAR_TASK or FLAG_ACTIVITY_NEW_TASK)
                            startActivity(i)
                        }
                        if (context is MainActivity)
                            setupCaseUI(basicCaseInfoList!!, context)

                    } else {
                        when(response.code()) {
                            400 -> showErrorSnackBar("Error 400, Bad Request!")
                            404 -> showErrorSnackBar("Error 404, Page is not found!")
                            else -> showErrorSnackBar("Generic Error!")
                        }
                    }
                }

                override fun onFailure(call: Call<BasicCaseInfoResponse>, t: Throwable) {
                    // If user logs in with the wrong credentials
                    if ("MalformedJsonException" in t.toString()){
                        showErrorSnackBar("Bad user account")
                    } else
                        showErrorSnackBar("Network Exception occurred! ${t.toString()}")

                    hideProgressDialog()
                }
            })
        }
        else{
            Toast.makeText(context, "Network is not available!", Toast.LENGTH_LONG).show()
            if (!isNetworkAvailable(context) && context is SplashActivity && isUserSignedIn())
                startActivity(Intent(context, MainActivity::class.java))
        }
    }

    // RecyclerView necessities
    private var adapter: CaseListAdapter? = null
    private var caseListItems: ArrayList<Case>? = null
    private var layoutManager: RecyclerView.LayoutManager? = null

    fun setupCaseUI(basicCaseInfo: BasicCaseInfoResponse, context: Context) {
        caseListItems = ArrayList<Case>()
        layoutManager = LinearLayoutManager(context)

        caseListItems = ArrayList(basicCaseInfo.cases.asReversed())

        adapter = CaseListAdapter(caseListItems!!, context)
        if (caseListItems!!.size != 0) {
            caseRecyclerView.visibility = View.VISIBLE
            noCasesTextView.visibility = View.GONE

            caseRecyclerView.layoutManager = layoutManager
            caseRecyclerView.adapter = adapter
        }
    }

    // Temporary way of storing credentials in the app
    // Further developments of this app should definitely use Firebase authentication services
    val PREFS_NAME = "userAuth"
    var userAuthPrefs: SharedPreferences? = null

    fun storeUserNameAndPassword(username: String, password: String) {
        /*
        0 or MODE_PRIVATE is the default mode, where the created file can only be accessed by the
        calling application (or all applications sharing the same user ID).
         */
        userAuthPrefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        var editor: SharedPreferences.Editor = userAuthPrefs!!.edit()

        editor.putString("username", username)
        editor.putString("password", password)
        editor.apply()
    }

    fun clearStoredUserNameAndPassword() {
        userAuthPrefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        var editor: SharedPreferences.Editor = userAuthPrefs!!.edit()

        editor.clear().apply()
    }

    fun isUserSignedIn(): Boolean {
        var userCheck:SharedPreferences = getSharedPreferences(PREFS_NAME, 0)
        return userCheck.contains("username")
    }

    fun getUsername(): String {
        var sharedPrefInfo:SharedPreferences = getSharedPreferences(PREFS_NAME, 0)
        return sharedPrefInfo.getString("username", "null")!!
    }

    fun getPassword(): String {
        var sharedPrefInfo:SharedPreferences = getSharedPreferences(PREFS_NAME, 0)
        return sharedPrefInfo.getString("password", "null")!!
    }

    /*
    This function is used to show the progress dialog with the title and message to user.
     */
    fun showProgressDialog(text: String) {
        mProgressDialog = Dialog(this)

        /*Set the screen content from a layout resource.
        The resource will be inflated, adding all top-level views to the screen.*/
        mProgressDialog.setContentView(R.layout.dialog_progress)

        mProgressDialog.progressTextView.text = text

        //Start the dialog and display it on screen.
        mProgressDialog.show()
    }

    /*
    This function is used to dismiss the progress dialog if it is visible to user.
     */
    fun hideProgressDialog() {
        mProgressDialog.dismiss()
    }

    fun showErrorSnackBar(message: String) {
        val snackBar =
            Snackbar.make(findViewById(android.R.id.content), message, Snackbar.LENGTH_LONG)
        val snackBarView = snackBar.view
        snackBarView.setBackgroundColor(
            ContextCompat.getColor(
                this@BaseActivity,
                R.color.snackbar_error_color
            )
        )
        snackBar.show()
    }

    fun isNetworkAvailable(context: Context): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val network = connectivityManager.activeNetwork ?: return false
            val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?:return false

            return when{
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> return true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> return true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> return true
                else -> false
            }

        } else {
            val networkInfo = connectivityManager.activeNetworkInfo
            return networkInfo != null && networkInfo.isConnectedOrConnecting
        }
    }

    // Displaying epoch time in human readable format
    val simpleDateFormat = SimpleDateFormat("dd MMMM yyyy, HH:mm", Locale.ENGLISH)
    fun getDateString(time: Long) : String = simpleDateFormat.format(time * 1000L)
}