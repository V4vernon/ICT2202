package com.csi_homies.byte_a_block.activities

import android.content.Intent
import android.graphics.BitmapFactory
import android.os.Bundle
import android.text.TextUtils
import android.widget.Toast
import com.csi_homies.byte_a_block.network.AddEvidencePost
import com.csi_homies.byte_a_block.utils.Constants
import kotlinx.android.synthetic.main.activity_add_evidence.*
import kotlinx.android.synthetic.main.activity_photographing_evidence.*
import kotlinx.android.synthetic.main.evidence_list_row.*
import retrofit2.Retrofit
import android.graphics.Bitmap
import android.util.Base64
import com.csi_homies.byte_a_block.models.add_evidence_request.AddEvidencePostRequest
import com.csi_homies.byte_a_block.models.add_evidence_request.DraftEvidenceInfo
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import com.csi_homies.byte_a_block.models.basic_case_info_response.Case
import com.google.gson.Gson
import java.io.ByteArrayOutputStream
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.converter.gson.GsonConverterFactory


class AddEvidenceActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_add_evidence)

        // Get Image file path from PhotographingEvidenceActivity
        val filePath = intent.getStringExtra(Constants.IMAGE_FILEPATH_ID)

        // Get Case Id for which case the evidence is being added to
        val caseId = intent.getIntExtra(Constants.SELECTED_CASE_ID_ID, 0)

        setupActionBar(intent.getStringExtra(Constants.SELECTED_CASE_NAME_ID).toString())

        submitEvidenceButton.setOnClickListener {
            var locationFound = locationFoundEditText.text.toString().trim()
            var evidenceType = evidenceTypeEditText.text.toString().trim()
            var evidenceSerialNo = serialNoEditText.text.toString().trim()
            var extraNotes = extraNotesEditText.text.toString().trim()
            if (caseId != 0 && filePath!= null &&!(TextUtils.isEmpty(locationFound)
                        || TextUtils.isEmpty(evidenceType)
                        || TextUtils.isEmpty(evidenceSerialNo)
                        || TextUtils.isEmpty(extraNotes))) {
                postEvidenceToWebServer(caseId, locationFound, evidenceType, evidenceSerialNo, extraNotes, filePath)

            } else
                Toast.makeText(this, "Please fill up all the fields!", Toast.LENGTH_LONG).show()
        }
    }

    private fun postEvidenceToWebServer(caseId: Int, locationOfEvidence:String, typeOfEvidence:String, serialNoOfEvidence:String, notesForEvidence:String, imagePathOfEvidence:String) {
        // Converting the image of the evidence into base64 String
        val imageOfEvidence = BitmapFactory.decodeFile(imagePathOfEvidence)
        val base64ImageOfEvidence = encodeImage(imageOfEvidence)

        if (isNetworkAvailable(this@AddEvidenceActivity)){
            // Create Retrofit
            val retrofit = Retrofit.Builder()
                .baseUrl(Constants.BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

            val service:AddEvidencePost = retrofit.create<AddEvidencePost>(AddEvidencePost::class.java)

            // Create JSON using JSONObject
            val listOfDraftEvidence = listOf(
                DraftEvidenceInfo(
                    1, locationOfEvidence,
                    typeOfEvidence, serialNoOfEvidence,
                    base64ImageOfEvidence.toString(),
                    "In Transit", notesForEvidence
                )
            )
            val addEvidenceJsonObject =
                AddEvidencePostRequest(caseId, getUsername(), listOfDraftEvidence)

            val listCall: Call<BasicCaseInfoResponse> = service.postNewEvidence(addEvidenceJsonObject)

            showProgressDialog("Uploading Evidence Data...")

            listCall.enqueue(object: Callback<BasicCaseInfoResponse>{
                override fun onResponse(
                    call: Call<BasicCaseInfoResponse>,
                    response: Response<BasicCaseInfoResponse>
                ) {
                    if (response.isSuccessful){
                        val basicCaseInfoList: BasicCaseInfoResponse? = response.body()

                        val currentCaseInfo: Case = basicCaseInfoList!!.cases[0]

                        val i = Intent(this@AddEvidenceActivity, CaseInfoActivity::class.java)
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
                    startActivity(Intent(this@AddEvidenceActivity, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK))
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

    private fun setupActionBar(caseName: String) {
        var actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.title = "Case $caseName"
            actionBar.setHomeAsUpIndicator(R.drawable.ic_white_color_back_24dp)
            actionBar.setDisplayHomeAsUpEnabled(true)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return super.onSupportNavigateUp()
    }


    override fun onBackPressed() {
        val goBackToCaseInfo = Intent(this@AddEvidenceActivity, CaseInfoActivity::class.java)
        goBackToCaseInfo.flags = Intent.FLAG_ACTIVITY_REORDER_TO_FRONT
        startActivityIfNeeded(goBackToCaseInfo, 0)
        finish()
    }
}