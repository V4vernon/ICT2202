package com.csi_homies.byte_a_block.network

import com.csi_homies.byte_a_block.models.add_evidence_request.AddEvidencePostRequest
import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

// POST, '/api/add_evidence/'
interface AddEvidencePost {

    @Headers("Content-Type: application/json")
    @POST("/api/add_evidence/")
    fun postNewEvidence(
        @Body addEvidencePostRequest: AddEvidencePostRequest
    ): Call<BasicCaseInfoResponse>
}