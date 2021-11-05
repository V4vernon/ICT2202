package com.csi_homies.byte_a_block.network

import com.csi_homies.byte_a_block.models.basic_case_info_response.BasicCaseInfoResponse
import com.csi_homies.byte_a_block.models.modify_evidence_status_request.ModifyEvidenceStatusPostRequest
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

interface ModifyEvidenceStatusPost {

    @Headers("Content-Type: application/json")
    @POST("/api/check_evidence/")
    fun postNewEvidenceStatus(
        @Body modifyEvidenceStatusPostRequest: ModifyEvidenceStatusPostRequest
    ): Call<BasicCaseInfoResponse>
}