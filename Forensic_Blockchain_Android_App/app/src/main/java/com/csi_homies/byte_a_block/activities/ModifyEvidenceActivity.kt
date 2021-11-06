package com.csi_homies.byte_a_block.activities

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.TextUtils
import android.util.Base64
import android.widget.ArrayAdapter
import android.widget.Toast
import com.csi_homies.byte_a_block.models.add_evidence_request.AddEvidencePostRequest
import com.csi_homies.byte_a_block.models.add_evidence_request.DraftEvidenceInfo
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import com.csi_homies.byte_a_block.models.basic_case_info_response.Case
import com.csi_homies.byte_a_block.models.modify_evidence_status_request.ModifyEvidenceStatusPostRequest
import com.csi_homies.byte_a_block.network.AddEvidencePost
import com.csi_homies.byte_a_block.network.ModifyEvidenceStatusPost
import com.csi_homies.byte_a_block.utils.Constants
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_modify_evidence.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.ByteArrayOutputStream

class ModifyEvidenceActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_modify_evidence)

        // Setup for the dropdown text box
        val newStatusDropDownItems = resources.getStringArray(R.array.new_evidence_status_options)
        val arrayAdapter = ArrayAdapter(this, R.layout.new_status_dropdown_item, newStatusDropDownItems)

        // Get Image file path from PhotographingEvidenceActivity
        val filePath = intent.getStringExtra(Constants.IMAGE_FILEPATH_ID)

        // Get Case Id for which case the evidence status being modified belongs to
        val caseId = intent.getIntExtra(Constants.SELECTED_CASE_ID_ID, 0)

        // Get Evidence Id for which evidence we are modifying status of
        val evidenceId = intent.getIntExtra(Constants.SELECTED_EVIDENCE_ID_ID, 0)

        setupActionBar(evidenceId.toString())

        newEvidenceStatusAutoCompText.setAdapter(arrayAdapter)

        modifyEvidenceStatusButton.setOnClickListener {
            var newEvidenceStatus = newEvidenceStatusAutoCompText.text.toString().trim()
            var newStatusPurpose = newEvidencePurposeEditText.text.toString().trim()

            if (caseId != 0 && evidenceId != 0 && filePath!= null &&
                        !(TextUtils.isEmpty(newEvidenceStatus) || TextUtils.isEmpty(newStatusPurpose))) {
                postNewEvidenceStatusToWebServer(caseId, evidenceId, newEvidenceStatus, newStatusPurpose, filePath)
            } else
                Toast.makeText(this, "Please fill up all the fields!", Toast.LENGTH_LONG).show()
        }
    }

    private fun postNewEvidenceStatusToWebServer(caseId: Int, evidId:Int, newStatus:String, newStatusPurpose:String, imagePathOfEvidence:String) {
        // Converting the image of the evidence into base64 String
        val imageOfEvidence = BitmapFactory.decodeFile(imagePathOfEvidence)
        val base64ImageOfEvidence = encodeImage(imageOfEvidence)

        if (isNetworkAvailable(this@ModifyEvidenceActivity)){
            // Create Retrofit
            val retrofit = Retrofit.Builder()
                .baseUrl(Constants.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

            val service: ModifyEvidenceStatusPost = retrofit.create<ModifyEvidenceStatusPost>(ModifyEvidenceStatusPost::class.java)

            // Create JSON using JSONObject
            val newEvidenceStatusJsonObject =
                ModifyEvidenceStatusPostRequest(
                    caseId, evidId, getUsername(),
                    newStatus, newStatusPurpose,
                    base64ImageOfEvidence.toString()
                )

            val listCall: Call<BasicCaseInfoResponse> = service.postNewEvidenceStatus(newEvidenceStatusJsonObject)

            showProgressDialog("Modifying Evidence Status...")

            listCall.enqueue(object: Callback<BasicCaseInfoResponse> {
                override fun onResponse(
                    call: Call<BasicCaseInfoResponse>,
                    response: Response<BasicCaseInfoResponse>
                ) {
                    if (response.isSuccessful){
                        val basicCaseInfoList: BasicCaseInfoResponse? = response.body()

                        val currentCaseInfo: Case = basicCaseInfoList!!.cases[0]

                        val i = Intent(this@ModifyEvidenceActivity, CaseInfoActivity::class.java)
                        i.putExtra(Constants.SELECTED_CASE_INFO_ID, Gson().toJson(currentCaseInfo))
                        startActivity(i)
                        finish()

                        hideProgressDialog()

                    } else {
                        when(response.code()) {
                            400 -> showErrorSnackBar("Error 400, Bad Request!")
                            404 -> showErrorSnackBar("Error 404, Page is not found!")
                            else -> showErrorSnackBar("Generic Error!")
                        }
                    }
                }

                override fun onFailure(call: Call<BasicCaseInfoResponse>, t: Throwable) {
                    showErrorSnackBar("Network Exception occurred! ${t.toString()}")
                    startActivity(Intent(this@ModifyEvidenceActivity, MainActivity::class.java))
                    finish()
                    hideProgressDialog()
                }
            })
        }
    }

    private fun encodeImage(bm: Bitmap): String? {
        val baos = ByteArrayOutputStream()
        bm.compress(Bitmap.CompressFormat.JPEG, 100, baos)
        val b = baos.toByteArray()
        return Base64.encodeToString(b, Base64.DEFAULT)
    }

    private fun setupActionBar(evidId: String) {
        var actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.title = "Modify Evidence $evidId Status"
            actionBar.setHomeAsUpIndicator(R.drawable.ic_white_color_back_24dp)
            actionBar.setDisplayHomeAsUpEnabled(true)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return super.onSupportNavigateUp()
    }

    override fun onBackPressed() {
        val goBackToEvidenceInfo = Intent(this@ModifyEvidenceActivity, EvidenceInfoActivity::class.java)
        goBackToEvidenceInfo.flags = Intent.FLAG_ACTIVITY_REORDER_TO_FRONT
        startActivityIfNeeded(goBackToEvidenceInfo, 0)
        finish()
    }
}